from rest_framework.response import Response
from rest_framework import status
import replicate

def get_ai_prompt(request):
    print(request.body)
    output = replicate.run(
    "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
    input={"prompt": f"{request.body}"}
    )
    return Response("completed", status=status.HTTP_200_OK)



