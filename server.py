# -*- coding: utf-8 -*-
from config import DEBUG
from app import app

app.run(debug=DEBUG, host='0.0.0.0')