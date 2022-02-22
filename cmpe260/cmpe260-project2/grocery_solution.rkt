#lang scheme
;2016400048
;ömer faruk özdemir


(define FARMS '(
(farmA 100 (apricot apple blueberry))
(farmB 90 (broccoli carrot grape))
(farmC 75 (corn grape lemon))
(farmD 75 ())
(farmE 45 (lemon melon olive berry))
(farmF 70 (lemon carrot))
(farmG 50 (olive))
(farmH 150 (olive grape apple))
(farmI 50 (apple))
))

(define CUSTOMERS '(
(john (farmA farmC) (apricot lemon))
(james (farmB farmC) (grape corn))
(arya (farmB farmD) (grape broccoli))
(elenor () ())
(alan (farmG farmH) (olive apple))
(george (farmF farmE farmG) (lemon melon olive apple))
(cersei (farmE farmF farmH farmI) (lemon olive apple))
(jon (farmA farmB farmC farmD farmE farmF farmG farmH farmI) (apricot apple blueberry broccoli carrot grape corn lemon melon olive berry))
))

(define CROPS '(
(apricot farmA 10)
(apple farmA 12)
(melon farmE 22)
(olive farmE 40)
(berry farmE 10)
(lemon farmF 35)
(carrot farmF 5)
(olive farmG 60)
(olive farmH 30)
(blueberry farmA 15)
(broccoli farmB 8)
(carrot farmB 5)
(grape farmB 10)
(corn farmC 9)
(grape farmC 12)
(lemon farmC 10)
(lemon farmE 12)
(grape farmH 10)
(apple farmH 8)
(apple farmI 8)
))



(define (TRANSPORTATION-COST name)  ( searchSecond FARMS name) ) 

(define (searchSecond list name)
   (cond  
         ( (eqv?(length list) 0) 0) 
         ( (eqv?(car(car list)) name) (car(cdr(car list))) )
         (else (searchSecond (cdr list) name))
  )
)

(define (AVAILABLE-CROPS name) (searchThird FARMS name) )                                      

(define (searchThird list name)
   (cond  
         ((eqv?(length list) 0) '()) 
         ( (eqv?(car(car list)) name) (caddar list) ) 
         (else (searchThird (cdr list) name))
  )
)

(define (INTERESTED-CROPS name) (searchThird CUSTOMERS name))


(define (CONTRACT-FARMS name) (searchSecondList CUSTOMERS name))

(define (searchSecondList list name)
   (cond  
         ((eqv?(length list) 0) '()) 
         ( (eqv?(car(car list)) name) (car(cdr(car list))) )
         (else (searchSecondList (cdr list) name))
  )
)

(define(CONTRACT-WITH-FARM name) (createFarmList CUSTOMERS name))

(define (createFarmList list name) 
    (cond
        ( (eqv? (length list) 0) '())
        ( (member (cadar list) name) (cons (caar list) (createFarmList (cdr list) name)) )
        ( else (createFarmList (cdr list) name))
    )
)


(define (member list name)
    (cond
        ( (eqv? (length list) 0) #f)
        ( (eqv? (car list) name) #t)
        (else (member (cdr list) name) )
    )
)

(define  (INTERESTED-IN-CROP name) (createCustomersList CUSTOMERS name))

(define (createCustomersList list name) 
    (cond
        ( (eqv? (length list) 0) '())
        ( (member (caddar list) name) (cons (caar list) (createCustomersList (cdr list) name)) )
        ( else (createCustomersList (cdr list) name))
    )
)

(define(MIN-SALE-PRICE name) (findMinPrice(createPriceList CROPS name)))

(define (createPriceList list name) 
    (cond
        ( (eqv? (length list) 0) '())
        ( (eqv? (caar list) name) (cons (caddar list) (createPriceList (cdr list) name) ) )
        ( else (createPriceList (cdr list) name) )
    )
)

(define (findMinPrice list)
    (cond
        ( (eqv? (length list) 1) (car list) )
        ( (eqv? (length list) 0) 0 ) 
        ( else (min (car list) (findMinPrice (cdr list) ) ) )
    )
)

(define (CROPS-BETWEEN minPrice maxPrice) (myCropsBetween CROPS minPrice maxPrice) )


(define (myCropsBetween List minPrice maxPrice)
    (cond 
        ( (eqv? (length List) 0) '() )
        ( ( and (and (>= (caddar List) minPrice) (<= (caddar List) maxPrice) ) (not (member (myCropsBetween (cdr List) minPrice maxPrice) (caar List) ) ) ) (cons (caar List) (myCropsBetween (cdr List) minPrice maxPrice))  )
        ( else (myCropsBetween (cdr List) minPrice maxPrice) )
    )
)


(define (betweenPrices price minPrice maxPrice crop) 
    ( if (and (>= price minPrice) (<= price maxPrice) )
        (cons crop '())
        '()
    )
)

(define (BUY-PRICE name crop) (findMinPrice (createPrices (CONTRACT-FARMS name) crop)))

(define (createPrices farms crop)
    ( if (eqv? (length farms) 0)
        '()
        (if (member (AVAILABLE-CROPS (car farms)) crop) 
            (cons (finalPrice (car farms) crop) (createPrices (cdr farms) crop) ) 
            (createPrices (cdr farms) crop)
        ) 
    )
)
    
(define (finalPrice farm crop)(+ (TRANSPORTATION-COST farm) (findPrice CROPS farm crop)) )
    
(define (findPrice list farm crop)
    (cond
        ( (eqv? (length list) 0) 0) 
        ( ( and (eqv? (caar list) crop) (eqv? (cadar list) farm) ) (caddar list) )
        (else (findPrice (cdr list) farm crop ) )
    )
)


(define (TOTAL-PRICE name) (sumPrices (INTERESTED-CROPS name ) name ) )

(define (sumPrices list name) 
    (cond
        ( (eqv? (length list) 0) 0 ) 
        ( else (+ (BUY-PRICE  name (car list)) (sumPrices (cdr list) name ) ) )
    )
)