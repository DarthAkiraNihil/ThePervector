import argparse
from the_pervector import ThePervector

parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument('job_id', type=int, help='Input dir for videos')
parser.add_argument('token', type=str, help='Output dir for image')
parser.add_argument('chat_id', type=int, help='Output dir for image')
parser.add_argument('provider', type=str, help='Output dir for image')
parser.add_argument('service', type=str, help='Output dir for image')
parser.add_argument('creator_id', type=str, help='Output dir for image')
args = parser.parse_args()

ThePervector(args.job_id, args.token, args.chat_id).download_and_send(args.provider, args.service, args.creator_id)
