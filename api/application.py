from flask import Flask
from flask_restful import Api, Resource, reqparse

app=Flask(__name__)
api=Api(app)

videos={}
video_put_args=reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is missing", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=False)
video_put_args.add_argument("views", type=int, help="Views on the video is missing", required=True)



class Video(Resource):
    def get(self,video_id):
        if video_id in videos:
            return videos[video_id]
        else:
            return f"Video with video_id:{video_id} not found"
        
    def put(self,video_id):
        args= video_put_args.parse_args()
        return {video_id: args}
        
api.add_resource(Video,"/video/video_id=<int:video_id>")

if __name__=="__main__":
    app.run(debug=True)



#Practice
# names={"Priya":{"age":23,"gender":"female","hobby":"Reading Novels"},
#        "Soham":{"age":23, "gender":"male","hobby":"Playing Guitar"}}

# class HelloWorld(Resource):
#     def get(self,name):
#         if name in names:
#             return names[name]
#         else: 
#             return "Name Not Found"

#     # def get(self,name,test):
#     #     return f"Hello {name}, test number {test}!"
    
#     # def post(self):
#     #     return {"post_data":"Priya"}
    
# api.add_resource(HelloWorld,"/hello/<string:name>")
# #api.add_resource(HelloWorld,"/hello/<string:name>/<int:test>")    

'''
If you want to use request.form[] instead of reqparser. You can do it this way:
from flask import Flask, request, jsonify

app = Flask(__name__)

videos = {}

@app.route('/video/<int:video_id>', methods=['POST'])
def add_video(video_id):
    # Initialize an errors dictionary
    errors = {}

    # Extract and validate data from request.form
    name = request.form.get("name")
    if not name:
        errors["name"] = "Name is required and must be a string."

    views = request.form.get("views")
    try:
        views = int(views) if views else None
        if views is None:
            errors["views"] = "Views are required and must be an integer."
    except ValueError:
        errors["views"] = "Views must be a valid integer."

    likes = request.form.get("likes", 0)  # Default value is 0 if not provided
    try:
        likes = int(likes)
    except ValueError:
        errors["likes"] = "Likes must be a valid integer."

    # If there are errors, return a 400 response with the errors
    if errors:
        return jsonify({"errors": errors}), 400

    # If no errors, add the video to the database
    videos[video_id] = {
        "name": name,
        "views": views,
        "likes": likes
    }
    return jsonify(videos[video_id]), 201


if __name__ == "__main__":
    app.run(debug=True)

'''