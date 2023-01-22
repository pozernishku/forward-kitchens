# forward-kitchens
Reverse engineering [home task](https://forwardkitchens.notion.site/forwardkitchens/Reverse-Engineering-Take-Home-Assignment-a15843a2763f4bc6a9ee554f57ff2720)
from Forward Kitchens

# Install
1. Run ```git clone https://github.com/pozernishku/forward-kitchens.git```
2. Move into project directory ```cd forward-kitchens```
3. To install project dependencies, run ```poetry install``` (this command requires [poetry to be installed](https://python-poetry.org/docs/#installation))
4. Create an environment file ```.env``` with the following secrets (ask [me](https://t.me/zackushka))
   - ```SMARTPROXY_USER=...```
   - ```SMARTPROXY_PASSWORD=...```
5. Activate environment ```poetry shell```

# Run
1. Move to the ```crawl``` directory of the project ```cd crawl```
2. Run ```scrapy crawl grubhub_spider --nolog -a restaurant_url="URL" -O ../crawl_output/us/grubhub_spider/grubhub_spider__output.csv```
   - Use any [restaurant URL](https://www.grubhub.com/restaurant/mezeh-optimist-hall-340-e-16th-st-unit-r201-charlotte/2809951) in ```-a restaurant_url="URL"```
3. Check the output in ```grubhub_spider__output.csv```
