from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form

from app.http import deps
from app.http.deps import get_db
from app.models.fusion import Fusion
from app.schemas.fusion import FusionDetail, FusionDetail_m, FusionCreate, FusionUpdate

import websocket  # websocket-client (https://github.com/websocket-client/websocket-client)
import requests
import random
import logging
import uuid

from obs import ObsClient
import os

server_address = "u486816-ac4b-dad91b77.westc.gpuhub.com:8443"
server_style_image_path = "style.png"
server_sketch_image_path = "sketch.png"
client_id = str(uuid.uuid4())

# 设置 AK/SK
ak = os.getenv("AccessKeyID")
sk = os.getenv("SecretAccessKey")
server = "https://obs.cn-south-1.myhuaweicloud.com"
bucket_name = "artist-eyes"

router = APIRouter(
    prefix="/fusions"
)

# 创建 obsClient 实例
obsClient = ObsClient(access_key_id=ak, secret_access_key=sk, server=server)


# 将前端传来的图片上传到华为云的OBS存储桶中
@router.post("/obs", response_model=FusionDetail_m, dependencies=[Depends(get_db)])
async def upload_obs_image(
        image: UploadFile = File(...),   # 接收前端上传的文件
        username: str = Form(...),       # 接收表单中的用户名
        user_id: int = Form(...),        # 接收表单中的用户ID
        artist_id: int = Form(...),      # 接收表单中的艺术家ID
    ):
    '''
    将前端传来的图片上传到华为云的OBS存储桶中
    '''
    
    if not image:
        return jsonify({"error": "No file provided"}), 400

    temp_dir = './tmp'
    os.makedirs(temp_dir, exist_ok=True)  # 创建目录，若不存在

    file_location = os.path.join(temp_dir, image.filename)

    # 获取上传的文件的内容
    file_location = f'./tmp/{image.filename}'  # 临时存储路径

    # 将文件保存到临时路径
    with open(file_location, 'wb') as buffer:
        buffer.write(await image.read())

    # logging.info(f'接收到图片并保存到: {file_location}')

    try:
        # 上传文件到 OBS
        object_key = f'user/{username}/{image.filename}'  # 使用用户名作为路径的一部分
        resp = obsClient.putFile(bucket_name, object_key, file_location)
        if resp.status < 300:
            logging.info(f"文件上传OBS成功: {resp.body.objectUrl}")

            draft_url = resp.body.objectUrl
            # 数据库添加一条新的融合数据
            fusion = Fusion.create(
                user_id=user_id,
                artist_id=artist_id,
                draft=draft_url
            )
            return fusion

    finally:
        # 删除临时文件
        if os.path.exists(file_location):
            os.remove(file_location)


# 生成融合图片
@router.post("/generate")
def create_fusion(content_p, user_name, sketch_src, style_src):
    """
    生成融合图片，创建一个新的融合记录
    """

    # 加载 JSON 配置
    with open('../../providers/comfyui_api_chinese.json','r', encoding='utf-8') as f:
        prompt = json.load(f)

    # 设置文本提示
    prompt["143"]["inputs"]["text"] = content_p
    prompt["7"]["inputs"]["text"] = (
        "NSFW, (worst quality:2), (low quality:2), (normal quality:2), lowres, "
        "normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, "
        "(ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, "
        "(poorly drawn hands:1.5), blurry, (bad anatomy:1.21), (bad proportions:1.331), extra limbs, "
        "(disfigured:1.331), (missing arms:1.331), (extra legs:1.331), (fused fingers:1.61051), "
        "(too many fingers:1.61051), (unclear eyes:1.331), lowers, bad hands, missing fingers, extra digit,"
        "bad hands, missing fingers, (((extra arms and legs))),"
    )

    prompt["119"]["inputs"]["image"] = 'sketch.png'
    prompt["21"]["inputs"]["image"] = 'style.png'

    # 设置随机种子
    seednum = random.randint(1, 10000)
    prompt["127"]["inputs"]["seed"] = seednum

    ws = websocket.WebSocket()

    # 连接 WebSocket
    try:
        ws.connect("wss://{}/ws?clientId={}".format(server_address, client_id))
        logging.info("WebSocket connection established")
    except Exception as e:
        logging.error(f"WebSocket connection failed: {e}")
        return

    # 将本地上传的图片上传到云服务器
    upload_image(style_src, server_style_image_path)
    upload_image(sketch_src, server_sketch_image_path)

    # 获取图片
    images = get_images(ws, prompt)

    # 保存图片到用户文件夹
    for node_id in images:
        for image_data in images[node_id]:
            from PIL import Image
            import io
            image = Image.open(io.BytesIO(image_data))
            image.save(f"./static/user_data/{user_name}/final_paint/artwork.png")
            logging.info("Image saved for user %s", user_name)

    fusion = Fusion.create(
        user_id=request_data.user_id,
        phase_id=request_data.phase_id,
        draft=request_data.draft,
        time=request_data.time
    )
    return fusion


# 获取所有融合记录
@router.get("/", response_model=list[FusionDetail_m], dependencies=[Depends(get_db)])
def get_fusions(skip: int = 0, limit: int = 10):
    """
    获取所有融合记录列表
    """
    fusions = Fusion.select().offset(skip).limit(limit)
    return list(fusions)


# 根据 ID 获取单个融合记录信息
@router.get("/{fusion_id}", response_model=FusionDetail_m, dependencies=[Depends(get_db)])
def get_fusion(fusion_id: int):
    """
    根据融合记录 ID 获取信息
    """
    fusion = Fusion.get_or_none(Fusion.id == fusion_id)
    if not fusion:
        raise HTTPException(status_code=404, detail="融合记录未找到")
    return fusion


# 根据用户 ID 获取所有融合记录
@router.get("/user/{user_id}", response_model=list[FusionDetail_m], dependencies=[Depends(get_db)])
def get_fusions_by_user(user_id: int):
    """
    根据用户 ID 获取所有融合记录
    """
    # 查询所有与该用户关联的融合记录
    fusions = Fusion.select().where(Fusion.user_id == user_id)

    if not fusions:
        raise HTTPException(status_code=404, detail="融合记录未找到")
    
    return list(fusions)


# 创建新融合记录
@router.post("/", response_model=FusionDetail_m, dependencies=[Depends(get_db)])
def create_fusion(request_data: FusionCreate):
    """
    创建一个新的融合记录
    """
    fusion = Fusion.create(
        user_id=request_data.user_id,
        phase_id=request_data.phase_id,
        draft=request_data.draft,
    )
    return fusion


# 更新融合记录
@router.put("/{fusion_id}", response_model=FusionDetail_m, dependencies=[Depends(get_db)])
def update_fusion(fusion_id: int, request_data: FusionUpdate):
    """
    更新融合记录信息
    """
    fusion = Fusion.get_or_none(Fusion.id == fusion_id)
    if not fusion:
        raise HTTPException(status_code=404, detail="融合记录未找到")

    fusion.fusion = request_data.fusion
    fusion.title = request_data.title
    fusion.description = request_data.description
    fusion.save()
    
    return fusion


# 删除融合记录
@router.delete("/{fusion_id}", response_model=dict, dependencies=[Depends(get_db)])
def delete_fusion(fusion_id: int):
    """
    删除融合记录
    """
    fusion = Fusion.get_or_none(Fusion.id == fusion_id)
    if not fusion:
        raise HTTPException(status_code=404, detail="融合记录未找到")

    fusion.delete_instance()
    return {"msg": "融合记录已删除"}


