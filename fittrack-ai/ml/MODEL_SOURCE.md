# Pretrained baseline provenance

Model: onnx-community/swin-finetuned-food101-ONNX
Source: https://huggingface.co/onnx-community/swin-finetuned-food101-ONNX
Pinned revision: e5e50bfc6425aa546f3b4421ca8bd79d0dd610b8
File: onnx/model_q4.onnx (60.4 MB)
SHA-256: acfbf2d19eed6c5ede07c8d50c08f53efbaf2808ca74c144c154b6ba50db2881
Declared model license: Apache-2.0
Original fine-tuned model: aspis/swin-finetuned-food101, based on microsoft/swin-base-patch4-window7-224.

This artifact is a published pretrained Food-101 model. It is not custom FitTrack training, a complete Indian-food model, a detector/segmenter or a portion measurement system. The upstream model's reported benchmark is not presented as FitTrack's measured accuracy. No benchmark accuracy claim is made for this package.

Weights are not bundled in the small source ZIP. The Docker model-image build and `python -m ml.download_baseline` download the pinned artifact and verify its checksum. Runtime inference and the image/API chain were actually tested in the delivery environment.

Unknown heuristic: return no candidate when the largest softmax score is below 0.4 or entropy is above 3.0. These are engineering defaults, not calibrated uncertainty guarantees. A high-scoring out-of-scope photo may still be wrong, so manual user confirmation is mandatory.

Image processing resizes to 224×224, rescales RGB to [0,1], then uses the source model's mean/std and NCHW layout. No serving mass is inferred. The model runs on CPU through ONNX Runtime; raw photographs are not retained or sent to an external inference provider.
