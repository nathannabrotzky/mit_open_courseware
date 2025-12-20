(format t "Running ps0.lisp . . . ~%")

-37

(* 3 4)

(> 10 9.7)

(- (if (> 3 4)
       7
       10)
   (/ 16 10))

(* (- 25 20)
   (+ 6 3))

+

(defun double-val (x) (* 2 x))

(defvar c 4)

c

(double-val c)

c

(double-val (double-val (+ c 5)))

(defun times-2 (x) (double-val x))

(times-2 c)

(defvar d c)

(= c d)

(cond ((>= c 2) d)
      ((= c (- d 5)) (+ c d))
      (t (abs (- c d))))
