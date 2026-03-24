from pathlib import Path


def run_catvton(
        user_image_path: Path,
        garment_path: Path,
        output_path: Path,
):
    """
    실제 CatVTON 추론 실행부.
    현재는 빈 구현으로, 모델 연동 시 여기에 CatVTON 파이프라인 삽입.
    """
    # TODO: CatVTON 모델 로딩 및 추론 코드 삽입
    # 예시:
    # from diffusers import StableDiffusionInpaintPipeline
    # pipeline = load_catvton_pipeline()
    # result = pipeline(user_image=user_image_path, garment=garment_path)
    # result.save(output_path)

    raise NotImplementedError(
        "CatVTON runner is not implemented yet. Set USE_MOCK=true for demo mode."
    )
