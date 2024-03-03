from rvc_python.infer import infer_file, infer_files

# To process a single file:
result = infer_file(
    input_path="./speech.mp3",
    model_path="./model/model.pth",
    index_path="",  # Optional: specify path to index file if available
    device="cpu:0",  # Use cpu or cuda
    f0method="harvest",  # Choose between 'harvest', 'crepe', 'rmvpe', 'pm'
    # Transpose setting
    # Output file path
    index_rate=0.5,
    filter_radius=3,
    resample_sr=0,  # Set to desired sample rate or 0 for no resampling.
    rms_mix_rate=0.25,
    protect=0.33,
    version="v2"
)

print("Inference completed. Output saved to:", result)
