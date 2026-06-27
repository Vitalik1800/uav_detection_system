import os

from ultralytics import YOLO


# =========================================
# SETTINGS
# =========================================

DATA_YAML = "dataset/data.yaml"


# =========================================
# TRAIN STAGE
# =========================================

def train_stage(
    stage_name,
    model_path,
    epochs,
    imgsz,
    patience,
    mosaic,
    close_mosaic,
    scale,
    translate,
    fliplr
):

    stage_dir = f"runs/detect/{stage_name}"

    last_weights = (
        f"{stage_dir}/weights/last.pt"
    )

    best_weights = (
        f"{stage_dir}/weights/best.pt"
    )

    print("\n" + "=" * 60)
    print(f"STARTING: {stage_name}")
    print("=" * 60 + "\n")

    # =====================================
    # RESUME TRAINING
    # =====================================

    if os.path.exists(last_weights):

        print(
            f"[INFO] Resume from:\n"
            f"{last_weights}\n"
        )

        model = YOLO(last_weights)

        model.train(
            resume=True
        )

    # =====================================
    # NEW TRAINING
    # =====================================

    else:

        print(
            f"[INFO] New training stage:\n"
            f"{stage_name}\n"
        )

        if not os.path.exists(model_path):

            raise FileNotFoundError(
                f"Model not found:\n{model_path}"
            )

        model = YOLO(model_path)

        model.train(

            # Dataset
            data=DATA_YAML,

            # Training
            epochs=epochs,

            imgsz=imgsz,

            batch=2,

            # CPU
            workers=0,
            cache=False,

            device="cpu",

            amp=False,

            # Early stopping
            patience=patience,

            # Augmentations
            fliplr=fliplr,

            scale=scale,

            translate=translate,

            mosaic=mosaic,

            close_mosaic=close_mosaic,

            # Save name
            name=stage_name
        )

    # =====================================
    # VERIFY BEST MODEL
    # =====================================

    if not os.path.exists(best_weights):

        raise FileNotFoundError(
            f"Best model not found:\n"
            f"{best_weights}"
        )

    print(
        f"\n[INFO] Stage completed:\n"
        f"{stage_name}"
    )

    print(
        f"[INFO] Best weights:\n"
        f"{best_weights}\n"
    )

    return best_weights


# =========================================
# MAIN
# =========================================

def main():

    print("\nChecking dataset...\n")

    if not os.path.exists(DATA_YAML):

        raise FileNotFoundError(
            f"Dataset YAML not found:\n"
            f"{DATA_YAML}"
        )

    # =====================================
    # STAGE 1
    # FAST WARMUP
    # =====================================

    stage1_best = train_stage(

        stage_name="uav_stage1",

        model_path="yolov8n.pt",

        epochs=5,

        imgsz=320,

        patience=3,

        mosaic=0.3,

        close_mosaic=2,

        scale=0.20,

        translate=0.05,

        fliplr=0.5
    )

    # =====================================
    # STAGE 2
    # MAIN LEARNING
    # =====================================

    stage2_best = train_stage(

        stage_name="uav_stage2",

        model_path=stage1_best,

        epochs=8,

        imgsz=416,

        patience=5,

        mosaic=0.5,

        close_mosaic=5,

        scale=0.30,

        translate=0.10,

        fliplr=0.5
    )

    # =====================================
    # STAGE 3
    # REFINEMENT
    # =====================================

    stage3_best = train_stage(

        stage_name="uav_stage3",

        model_path=stage2_best,

        epochs=10,

        imgsz=512,

        patience=5,

        mosaic=0.1,

        close_mosaic=3,

        scale=0.15,

        translate=0.05,

        fliplr=0.5
    )

    # =====================================
    # STAGE 4
    # FINAL STABILIZATION
    # =====================================

    stage4_best = train_stage(

        stage_name="uav_stage4",

        model_path=stage3_best,

        epochs=5,

        imgsz=640,

        patience=3,

        mosaic=0.0,

        close_mosaic=0,

        scale=0.05,

        translate=0.02,

        fliplr=0.0
    )

    print("\n" + "=" * 60)
    print("TRAINING COMPLETE")
    print("=" * 60)

    print("\nFINAL MODEL:\n")
    print(stage4_best)


# =========================================
# ENTRY POINT
# =========================================

if __name__ == "__main__":
    main()
