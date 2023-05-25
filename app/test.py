import pixellib
from pixellib.torchbackend.instance import instanceSegmentation

ins = instanceSegmentation()
ins.load_model("C:/Users/user/OneDrive/Desktop/3th_semester/thesis2/Coding/another_example/model/pointrend_resnet50.pkl")
result =ins.segmentImage('C:/Users/user/OneDrive/Desktop/3th_semester/thesis2/new_project_grpc/main-service/app/screenshot.jpg', show_bboxes=True, output_image_name="output_image.jpg")

my_dict = dict(result[0])

with open('result.txt', 'w') as file:
    # Write the dictionary content to the file
    for key, values in my_dict["object_counts"].items():
        values_str = str(values)
        file.write(f"{key}: {values_str}\n")