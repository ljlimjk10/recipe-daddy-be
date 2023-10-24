from django.http import HttpResponse
import replicate

def test(request):
    output = replicate.run(
    "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
    input={"prompt": "Hello Llams"}
    )
    for item in output:
        print(item)
