* [Reg](#reg)
    * [StringGet](#stringget)
    * [StringCount](#stringcount)
* [DateTime](#datetime)
    * [TimeSubtract](#timesubtract)
    * [ToDateTime](#todatetime)
* [OSBasic](#osbasic)
    * [CMD](#cmd)

# Reg

此部分function是使用正則表達式從data中提取特定字串時使用

## stringGet

* 字串獲得 (StringGet)
    1. 此function可以處理字串中多行的情況
    2. 可使用正則中群組功能
    3. 各參數皆以 "," 做區隔

    **輸入格式**
    ```sh
    :Utility2.StringGet,"輸入資料","正則pattern","分組組號","預計獲得參數個數"
    ```
    _輸入資料: 輸入需要拆解的字串_

    _正則 pattern: 想使用的正則 pattern，請使用原始字串(@後的字串)_

        範例:
        * ^0/(?:[0-3])\s+(?:[^\s]+\s+)([^\s]+)      (O)
        * ^0/(?:[0-3])\\s+(?:[^\\s]+\\s+)([^\\s]+)  (X)
    
    _分組組號: 假設 pattern中有分組的話，填上想獲得的組號，如果組號不只一個，請用","進行分隔; 如果沒分組請填上0_

        範例 1:
        input = 0/0  QSGMII  Up  1G  Full  None  No  None  None  Link-Up
        * :Utility2.StringGet,"input","0/0\s+(\w+)\s+(\w+)","1,2","2"
        Output:
            result_1 = QSGMII
            result_2 = Up
    
    _預計獲得參數個數: 預計想從正則中獲得多少結果，如果得到的結果少於填入值的話將以""填入_


    **EXAMPLE**

    1. 尋找以下字串中 Port 0/0-0/3 Link那欄的值

    input_data = 

    ```sh
    Dev/Port    Mode     Link   Speed  Duplex    Loopback      Autoneg      FEC        Link Scan   Port Manager
    --        --------  -----   -----  ------  -------------  ---------  ----------   -----------  ------------

    0/0         QSGMII    Up     1G     Full        None        No         None          None       Link-Up      
    0/1         QSGMII    Up     1G     Full        None        No         None          None       Link-Up      
    0/2         QSGMII    Up     1G     Full        None        No         None          None       Link-Up      
    0/3         QSGMII    Up     1G     Full        None        No         None          None       Link-Up
    0/4         QSGMII    Up     1G     Full        None        No         None          None       Link-Up      
    0/5         QSGMII    Up     1G     Full        None        No         None          None       Link-Up 
    ```   
    ```sh
    input:

    :Utility2.StringGet,"*(input_data)","^0/(?:[0-3])\s+(?:[^\s]+\s+)([^\s]+)","1","4"
    ```

    ```sh
    output:
        result_1 = Up
        result_2 = Up
        result_3 = Up
        result_4 = Up
    ```
    2. 獲得以下字串中的年、月、日、時、分、秒

    input_data = 

    ```sh
    20201212063055
    ```
    ```sh
    input:

    :Utility2.StringGet,"*(input_data)","^(\d[[4]])(\d[[2]])(\d[[2]])(\d[[2]])(\d[[2]])(\d[[2]])","1,2,3,4,5,6","6"
    ```

    ```sh
    output:
        year = 2020
        month = 12
        day = 12
        hour = 06
        minute = 30
        second = 55
    ```
    **REMINDER**

    -  **正則 pattern中不能出現 "{" 和 "}" 符號，如果需要使用，請用 "[[" 和 "]]" 代替**

## StringCount

* 字串計算 (StringCount)
    1. 此function用來計算該參數在字串中的數量

    **輸入格式**
    ```sh
    :Utility2.StringGet,"輸入資料","正則pattern"
    ```

    **EXAMPLE**

    1. 尋找以下字串中 "ff" 的數量
    
    input_data = 

    ```sh
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 1
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 2
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 3
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 4
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 5
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 6
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 7
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 8
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 9
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 10
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 11
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 12
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 13
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 14
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 15
    ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff - 17
    ```
    ```sh
    input:

    :Utility2.StringGet,"*(input_data)","ff\s+"
    ```

    ```sh
    output:
        256
    ```

# DateTime

此部分function是用來做時間的相關計算

## TimeSubtract

* 時間相減 (TimeSubtract)

    **輸入**
    ```sh
    :Utility2.TimeSubtract,"start time","end time","time type"
    ```
    _start time & end time: 開始時間與結束時間_

        接受格式:
        * %Y-%m-%d %H:%M:%S  
        * %Y/%m/%d %H:%M:%S
        * %Y%m%d%H%M%S

    _time type: 輸出時間尺度_

        接受格式:
        * days (無條件進位)
        * hours
        * minutes
        * seconds
    
    **輸出**

        Reply: 0
        Ref: Value

    **EXAMPLE**

    ```sh
    input:
    :Utility2.TimeSubtract,"20230404000000","20230405000001","days"
    ```

    ```sh
    output:
    2
    ```

## ToDateTime

* 時間轉換 (ToDateTime)

    **輸入**
    ```sh
    :Utility2.ToDateTime,"year,mon,day,hour,minute,second"
    ```
    _year,mon,day,hour,minute,second: 各時間尺度_

        * 需皆為數字
        * 輸入參數需要6個
    
    **輸出**

        Reply: 0
        Ref: Value
    
    **EXAMPLE**

    ```sh
    input:
    :Utility2.ToDateTime,"2023,4,4,0,0,0"
    ```

    ```sh
    output:
    20230404000000
    ```

# OSBasic

此部分function主要是收錄電腦基本操作，包含CMD、check file等

## CMD

* 執行CMD命令 (CMD)

    **輸入**
    ```sh
    :Utility2.CMD,"file path","arguments","timeout(ms)"
    ```
    _sfile path: 應用程式路徑_

    _arguments: 輸入參數_

        多參數的話請以","分隔, 沒參數的話請填""
    
    _timeout(ms):超時時間_

        時間單位為ms, 如果沒timeout就填-1
    
    **輸出**
  
        normal:
            Reply: 0
            Ref: Return
        timeout:
            Reply: 1
            Ref: "The proccess time out!"
