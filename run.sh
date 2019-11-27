export PYTHONIOENCODING=utf-8
export CUDA_VISIBLE_DEVICES=1
python main.py \
    --do_train_and_eval \
    --model_dir experiments/debug \
    --nega_num 8 \
    --learning_rate 5e-5 \
    --batch_size 32 \
    --epoch_num 3
