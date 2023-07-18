# 初始化資料庫連線
import pymongo # 載入 pymongo 套件
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from waitress import serve
import torch
import os
# import your_model_module
uri = "mongodb+srv://Avol0305:Aa3748653@cluster0.fe7wn3k.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db=client.membersystem # 選擇操作mywebsite資料庫
print("資料庫連線成功")

if __name__ == "__main__":
    # 假設您的 Flask app 物件是 'app'
    serve(app, host='0.0.0.0', port=5000)
# 初始化 Flask 伺服器
from flask import *
app=Flask(
    __name__,
    static_folder="static", # 靜態檔案的資料名稱
    static_url_path="/static",# 靜態檔案對應的網址路徑
    )
# 處理路由
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html")
    else:
        return redirect("/")
# /error?msg=錯誤訊息
@app.route("/error")
def error():
    message=request.args.get("msg", "發生錯誤請聯繫客服")
    return render_template("error.html", message=message)

@app.route("/signup", methods=["POST"])
def signup():
    # 從前端接收資料
    nickname=request.form["nickname"]
    email=request.form["email"]
    password=request.form["password"]
    # 根據接收到的資料 , 和資料庫互動
    collection=db.users
    # 檢查是否有相同的註冊資料
    result=collection.find_one({
        "email":email
    })
    if result != None:
        return redirect("/error?msg=信箱已經被註冊")
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/")

@app.route("/signin", methods=["POST"])
def signin():
    # 從前端取得使用者輸入
    email=request.form["email"]
    password=request.form["password"]
    # 和資料庫作互動
    collection=db.users
    # 檢查信箱密碼是否正確
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}    
        ]
    })
    # 登入失敗,導向到錯誤頁面
    if result==None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    # 登入成功,在Session紀錄會員資訊,導向到會員頁面
    session["nickname"]=result["nickname"]
    return redirect("/member")

@app.route("/signout")
def signout():
    # 移除 Session 中的會員資訊
    del session["nickname"]
    return redirect("/")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]  # 獲取上傳的檔案
    if file:
        filename = file.filename  # 獲取檔案名稱
        save_path = os.path.join("uploadfile", filename)  # 指定儲存路徑，這裡假設將檔案存儲在名為 "uploads" 的資料夾中

        file.save(save_path)  # 儲存檔案到本地伺服器
        return "File uploaded successfully"
    else :
        return "No file uploaded"


#model = your_model_module.MyModel()  # 創建一個模型實例

# 載入已訓練好的模型參數
#model.load_state_dict(torch.load('model.pth'))
#model.eval()  # 設定模型為評估模式

#@app.route('/predict', methods=['POST'])
#def predict():
    # 接收請求資料
#    data = request.get_json()

    # 處理資料並進行模型推論
#    result = your_model_module.predict(data, model)

    # 將結果回傳給呼叫端
#    return jsonify(result)

#if __name__ == '__main__':
#    app.run()

app.secret_key="deep-high-resolution" # 設定 Session的密鑰
app.run(port=3000)

