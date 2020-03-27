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
- (廢案)型號：Logitech 羅技 C525 HD 網路視訊攝影機 https://www.eclife.com.tw/SSD/moreinfo_46585.htm
- 拍攝高度確認：55cm
- raspiberry pi 3B+
- raspberry camera module v2 8MP


## 主程式介紹
1. YY_app.ipynb：linebot運行主檔
2. yyGermination.py：API主程式
  - ```connect(ip, port, username, password, database)```：資料庫互動模組
    * ```connect_DB()```：連線資料庫並建立連線物件db, cursor，結束使用時請執行```db.close()```避免資源占用
    * ```user_follow(line_id, user_name, right_id)```：寫入訂閱頻道的人員資訊與權限(預設=0[測試身分])
    * ```get_menu_id(line_id)```：取得指定用戶應綁定的圖文選單
    * ```convert_image_to_byte(image)```：轉換要儲存至資料庫中的array.ndarray圖檔為byte格式
    * ```get_series()```：取得所有資料庫的品種資料
    * ```save_process(gerData)```：儲存操作主流程，資料型態為字典，gerData為用戶於lineBot上回覆之內容
    * ```get_raspi_data(photo_id)```：用photo_id取得樹莓派拍攝儲存的影像資料
    * ```save_germination_record(germination_record, result_list)```：儲存整體辨識結果(germination_record)與每個海綿的資訊(result_list)至資料庫
    * ```get_result(porcess_id)```：抓取整個操作主流程的所有紀錄與成果
    * ```artificial_identify(series_id)```：取得指定品種尚未人工判別過，最接近判斷閾值的數據
    * ```save_artificial_result(series_id, line_id, artificial_result)```：儲存人工判別的結果、操作人、時間等資訊至資料庫
    
  - ```par(ip, port, username, password)```：遠端對樹莓派下指令的模組
    * ```connect_raspi(photo_id)```：命令樹莓派運行test.py程式檔，執行拍照、儲存等動作，並指定資料編號 = photo_id
    
  - ```germination(series_id, thershold, percent)```：發芽率辨識模組
    * ```convert_photo(slice_img)```：進行成像轉換(灰階、高斯模糊、二元化)
    * ```caculate()```：計算每個海綿的發芽數量與整體比例
    * ```resize_photo(image)```：原始圖片調整(取得目標四頂點、圖像梯形轉正、圖像長寬格式化)
    * ```get_photo(image)```：引用convert_photo、caculate、resize_photo進行發芽率辨識並回傳結果
