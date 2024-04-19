import argparse

parser = argparse.ArgumentParser(description='Videos to images')
parser.add_argument('job_id', type=str, help='Input dir for videos')
parser.add_argument('token', type=str, help='Output dir for image')
parser.add_argument('chat_id', type=int, help='Output dir for image')
parser.add_argument('provider', type=str, help='Output dir for image')
parser.add_argument('service', type=str, help='Output dir for image')
parser.add_argument('creator_id', type=int, help='Output dir for image')
args = parser.parse_args()

print(args.service)
