# webDashboard
This script reads data from a csv file and presents them on a web dashboard.
![preview](https://user-images.githubusercontent.com/22216795/190348667-75b74867-0105-4102-b34c-18d7e2af7205.png)
## Usage
### with existing web-server
1. Clone repository into web directory
2. check if dashboard is displayed correctly
3. update file-paths in 
```python
dataFilePath = "./latest_values.dat"
jsonFilePath = "./data.json"
```
4. run updatate-routine
```bash
python updateJSON.py
```
### without existing web-server
1. Change Parameters in runServer.py
```python
hostName = "localhost"
serverPort = 80
dataFilePath = "./latest_values.dat"
```
2. start server
```bash
python runServer.py
```

