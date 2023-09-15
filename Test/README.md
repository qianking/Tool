*[Reg](#reg)
    *[stringGet](#stringget)



# Reg

## stringGet
### Background

此Dll用在需要從data中提取特定字串時使用，主要是使用正則表達式，因此要對於正則有一定熟悉度

## Install

將 RTCDateTime.dll 放入 Centinmani\API底下

在Script中，在DUTs頁面將"DLL:StringRegex.dll","Reg",""加到需要使用的站點的Connection

## Usage

* 獲得字串 (StringGet)
    1. 此function可以處理字串中多行的情況
    2. 可使用正則中群組功能
    3. 各參數皆以 "," 做區隔

    **輸入格式**
    ```sh
    :Reg.StringGet,"輸入資料","正則pattern","分組組號","預計獲得參數個數"
    ```
    _輸入資料: 輸入需要拆解的字串_

    _正則 pattern: 想使用的正則 pattern，請使用原始字串(@後的字串)_

        範例:
        * ^0/(?:[0-3])\s+(?:[^\s]+\s+)([^\s]+)      (O)
        * ^0/(?:[0-3])\\s+(?:[^\\s]+\\s+)([^\\s]+)  (X)
    
    _分組組號: 假設 pattern中有分組的話，填上想獲得的組號，如果組號不只一個，請用","進行分隔; 如果沒分組請填上0_

        範例 1:
        input = 0/0  QSGMII  Up  1G  Full  None  No  None  None  Link-Up
        * :Reg.StringGet,"input","0/0\s+(\w+)\s+(\w+)","1,2","2"
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

    :Reg.StringGet,"*(input_data)","^0/(?:[0-3])\s+(?:[^\s]+\s+)([^\s]+)","1","4"
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

    :Reg.StringGet,"*(input_data)","^(\d[[4]])(\d[[2]])(\d[[2]])(\d[[2]])(\d[[2]])(\d[[2]])","1,2,3,4,5,6","6"
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

* 計算字串 (StringCount)
    1. 此function用來計算該參數在字串中的數量

    **輸入格式**
    ```sh
    :Reg.StringGet,"輸入資料","正則pattern"
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

    :Reg.StringGet,"*(input_data)","ff\s+"
    ```

    ```sh
    output:
        256
    ```
