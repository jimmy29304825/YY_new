# YY_new
## 需求套件：
- opencv：偵測、調整影像用
- numpy：計算發芽率等大量數據使用
- matplotlib：繪圖呈現工具
- imutils：成像梯形轉正套件
- line-bot：lineBot不解釋

## 資料夾-germination
1. 發芽率辨識主檔
2. 圖像調整程式碼(梯形轉正、相素調整)
3. 測試環境程式碼(確認參數、閾值、圖片裁切另存)

## 資料夾-controlPi
1. 遠端控制樹莓派執行指令
  - 樹莓派需載入相關套件(sys)才能吃到console給的參數

## 資料夾-line
1. YY_app：API後台主檔
2. richmenu：圖文選單設定檔
3. 請自行新增serect_key
4. push_message：推播訊息檔(TBC)
5. 各種json檔(for YY_app回覆訊息用)自行參閱

## 攝影機
- 型號：Logitech 羅技 C525 HD 網路視訊攝影機 https://www.eclife.com.tw/SSD/moreinfo_46585.htm
- 拍攝高度確認：55cm


## 主程式介紹
1. YY_app.ipynb：linebot運行主檔
2. yyGermination.py：API主程式
  - connect：資料庫互動模組
    * 引用參數：```connect(ip, port, username, password, database)```
    * ```connect_DB()```：連線資料庫並建立連線物件db, cursor，結束使用時請執行```db.close()```避免資源占用
    * ```user_follow(line_id, user_name, right_id)```：寫入訂閱頻道的人員資訊與權限(預設=0[測試身分])
