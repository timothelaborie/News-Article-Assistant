import argparse
import os

import numpy as np
np.bool = bool


from flask import Flask
from flask_cors import CORS
from flask_restful import Resource
from flask_restful import Api
from flask import jsonify, make_response, send_file

cwd = os.getcwd()

import requests
from bs4 import BeautifulSoup, Comment

import base64

import os
PAT = os.environ.get("PAT")

import re



    

def get_ai_response(prompt):
    # import openai
    # openai.api_key = os.environ.get("OPENAI_API_KEY")
    # print("key:", openai.api_key)
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are a helpful assistant."
    #         },
    #         {
    #             "role": "user",
    #             "content": prompt
    #         }
    #         ],
    #     temperature=0.1,
    #     max_tokens=2000,
    #     top_p=0.95,
    # )
    # text = response.choices[0].message.content






    USER_ID = 'meta'
    APP_ID = 'Llama-2'

    MODEL_ID = 'llama2-7b-chat'
    MODEL_VERSION_ID = 'e52af5d6bc22445aa7a6761f327f7129'

    RAW = f"""<s>[INST] <<SYS>>

You are a helpful assistant. Always answer as helpfully as possible.

<</SYS>>

{prompt} [/INST]"""

    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=RAW,
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)


    output = post_model_outputs_response.outputs[0]
    print(output.data.text.raw)
    text = output.data.text.raw






    #sample text
#     text = f"""sample response for
# {prompt}"""

    

    return text







def get_ai_image(prompt):
    USER_ID = 'stability-ai'
    APP_ID = 'stable-diffusion-2'
    # Change these to whatever model and text URL you want to use
    MODEL_ID = 'stable-diffusion-xl'
    MODEL_VERSION_ID = '0c919cc1edfc455dbc96207753f178d7'


    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here
    image_data = post_model_outputs_response.outputs[0].data.image.base64

    # Encode the image data into a base64 string
    base64_encoded = base64.b64encode(image_data).decode('utf-8')

    # Return the base64-encoded image data
    base64_image = f"data:image/png;base64,{base64_encoded}"

    return base64_image







    


class GetSummary(Resource):
    def post(self, 
            original_text_64, 
            ):

        original_text = base64.b64decode(original_text_64).decode('utf-8', errors='ignore')[:2000]
        print("GetSummary original_text:", original_text)
        prompt = f"""Summarize this article: 
{original_text}"""
        response = get_ai_response(prompt)
        return jsonify({
            'response': response,
        })


class GetExtractedArguments(Resource):
    def post(self, 
            original_text_64, 
            ):

        original_text = base64.b64decode(original_text_64).decode('utf-8', errors='ignore')[:2000]
        print("GetExtractedArguments original_text:", original_text)
        prompt = f"""Find the arguments in this article and repeat them, each on their own line: 
{original_text}"""
        response = get_ai_response(prompt)
        return jsonify({
            'response': response,
        })


class GetSDprompt(Resource):
    def post(self, 
            original_text_64, 
            ):

        original_text = base64.b64decode(original_text_64).decode('utf-8', errors='ignore')[:2000]
        print("GetSDprompt original_text:", original_text)
        prompt = f"""Generate a stable diffusion prompt from this article:
{original_text}"""
        response = get_ai_response(prompt)
        return jsonify({
            'response': response,
        })


class GetSDimage(Resource):
    def post(self, 
            original_text_64, 
            ):

        original_text = base64.b64decode(original_text_64).decode('utf-8', errors='ignore')[:2000]
        print("GetSDimage original_text:", original_text)
        response = get_ai_image(original_text)
        return jsonify({
            'response': response,
        })




def create_app():
    app = Flask(__name__)  # static_url_path, static_folder, template_folder...
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*"}})


    api = Api(app)

    api.add_resource(GetSummary, "/api/summary/<string:original_text_64>")
    api.add_resource(GetExtractedArguments, "/api/extract/<string:original_text_64>")
    api.add_resource(GetSDprompt, "/api/generate_prompt/<string:original_text_64>")
    api.add_resource(GetSDimage, "/api/generate_image/<string:original_text_64>")


    @app.route('/version')
    def version():
        return f"Job ID: {os.environ['JOB_ID']}\nCommit ID: {os.environ['COMMIT_ID']}"

    return app


def start_server():
    print("Starting server...")
    parser = argparse.ArgumentParser()

    #python server.py --host 127.0.0.1 --port 8000 --debug

    # API flag
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="The host to run the server",
    )
    parser.add_argument(
        "--port",
        default=os.environ.get("PORT"),
        help="The port to run the server",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run Flask in debug mode",
    )

    args = parser.parse_args()

    server_app = create_app()

    server_app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == "__main__":
    start_server()
