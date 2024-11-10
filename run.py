import argparse
import dotenv
import json
from src.derivation import create_answer
from src.retrieval import initialize_model_bi_encoder, initialize_model_cross_encoder

dotenv.load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--question', type=str, required=True)
    parser.add_argument('--save_tree', type=bool, default=True)
    parser.add_argument('--retrieval_method', type=str, choices=['bi_encoder', 'cross_encoder'], default='bi_encoder')
    parser.add_argument('--model', type=str, choices=['opus', 'haiku'], default='opus')
    parser.add_argument('--temperature', type=float, default=0.0)
    return parser.parse_args()

def save_tree(tree):
    with open('derivation_tree.json', 'w', encoding='utf-8') as f:
        json.dump(tree, f)

if __name__ == '__main__':
    args = parse_args()

    # Initialize the retrieval model
    print("Initializing retrieval model...")
    if args.retrieval_method == 'bi_encoder':
        retrieval_model = initialize_model_bi_encoder()
    else:
        retrieval_model = initialize_model_cross_encoder()

    print("Creating answer for question:", args.question)
    answer, tree = create_answer(args.question, args.model, retrieval_model, temperature=args.temperature)

    if args.save_tree:
        print("Saving derivation tree...")
        save_tree(tree)

    print("Answer:", answer)