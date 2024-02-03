import os
from typing import Optional

from dotenv import load_dotenv


load_dotenv()

GEO_KEY: Optional[str] | str = os.getenv('GEO_KEY')
GEO_URL: Optional[str] | str = os.getenv('GEO_API_URL')
YAW_API: Optional[str] | str = os.getenv('API_YA_WEATHER')
YAW_URL: Optional[str] | str = os.getenv('YA_WEATHER_URL')
