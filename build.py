from questions import Q
import json
N=len(Q)
data=[]
for q,o,a,f in Q:
    data.append(f'DATA "{q}"')
    data.append('DATA ' + ", ".join(f'"{x}"' for x in o) + f', "{a}"')
    data.append(f'DATA "{f}"')
bas = r'''REM ============================================================
REM  VOLUSIA HISTORY QUIZ
REM  A retro QBasic trivia game about Volusia County, Florida
REM  by Jeep Michelle - New Smyrna Beach, FL
REM  Runs in QBasic 1.1, QuickBASIC 4.5, QB64 and QBJS
REM  https://github.com/RamJeepMichelle/volusia-history-quiz
REM ============================================================
DECLARE SUB WrapPrint (t$, fg%)
DECLARE SUB WaitKey ()
DECLARE SUB Banner ()

CONST TOTAL = @@N@@
CONST ASKED = 10
DIM SHARED Q$(1 TO TOTAL), A$(1 TO TOTAL, 1 TO 4), K$(1 TO TOTAL), F$(1 TO TOTAL)
DIM ORD(1 TO TOTAL)

RESTORE QuizData
FOR I = 1 TO TOTAL
  READ Q$(I)
  READ A$(I, 1), A$(I, 2), A$(I, 3), A$(I, 4), K$(I)
  READ F$(I)
  ORD(I) = I
NEXT I

RANDOMIZE TIMER
FOR I = TOTAL TO 2 STEP -1
  J = INT(RND * I) + 1
  T = ORD(I): ORD(I) = ORD(J): ORD(J) = T
NEXT I

SCREEN 0
WIDTH 80, 25
COLOR 15, 1: CLS
CALL Banner
COLOR 14, 1
LOCATE 12, 1
PRINT "         Ten questions about the history of Volusia County, Florida."
PRINT
COLOR 7, 1
PRINT "              Press A, B, C or D to answer. Press Q to quit."
PRINT
COLOR 11, 1
PRINT "                      Press any key to fire up the engine..."
CALL WaitKey

SCORE = 0
FOR N = 1 TO ASKED
  I = ORD(N)
  COLOR 15, 1: CLS
  COLOR 14, 1
  PRINT " VOLUSIA HISTORY QUIZ" + SPACE$(38) + "Question" + STR$(N) + " of" + STR$(ASKED)
  COLOR 9, 1
  PRINT STRING$(79, "=")
  PRINT
  CALL WrapPrint(Q$(I), 15)
  PRINT
  FOR C = 1 TO 4
    COLOR 11, 1: PRINT "   "; CHR$(64 + C); ") ";
    COLOR 7, 1: PRINT A$(I, C)
  NEXT C
  PRINT
  COLOR 10, 1: PRINT "   Your answer: ";
  DO
    G$ = UCASE$(INKEY$)
    IF G$ = "" THEN SLEEP 1
  LOOP UNTIL G$ = "A" OR G$ = "B" OR G$ = "C" OR G$ = "D" OR G$ = "Q"
  IF G$ = "Q" THEN EXIT FOR
  PRINT G$
  PRINT
  IF G$ = K$(I) THEN
    SCORE = SCORE + 1
    COLOR 10, 1: PRINT "   RIGHT! Nice driving."
  ELSE
    COLOR 12, 1
    PRINT "   Not quite. The answer is "; K$(I); ") "; A$(I, ASC(K$(I)) - 64)
  END IF
  PRINT
  COLOR 14, 1: PRINT "   Did you know?"
  CALL WrapPrint(F$(I), 7)
  PRINT
  COLOR 7, 1: PRINT "   Score:"; SCORE; "   Press any key for the next question..."
  CALL WaitKey
NEXT N

COLOR 15, 1: CLS
CALL Banner
LOCATE 11, 1
COLOR 14, 1
PRINT "                        FINAL SCORE:"; SCORE; "out of"; ASKED
PRINT
IF SCORE >= 10 THEN R$ = "HALIFAX HISTORIAN - you could give the museum tours!"
IF SCORE >= 7 AND SCORE <= 9 THEN R$ = "VOLUSIA LOCAL - you know your beach from your river."
IF SCORE >= 4 AND SCORE <= 6 THEN R$ = "SNOWBIRD - welcome back, stay a while and explore."
IF SCORE <= 3 THEN R$ = "TOURIST - time for a history day trip around Volusia!"
COLOR 11, 1
PRINT "   Your rank: "; R$
PRINT
COLOR 7, 1
PRINT "   Want to see this history for yourself? Visit the Halifax Historical"
PRINT "   Museum on Beach Street in Daytona Beach, or plan a Jeep history day at"
PRINT "   ramjeepmichelle.github.io/JeepFlorida"
PRINT
COLOR 10, 1
PRINT "   Looking for a Jeep for sale in New Smyrna Beach or Daytona Beach?"
COLOR 15, 1
PRINT "   Jeep Michelle - New Smyrna Chrysler Jeep Dodge Ram, 2555 State Rd 44"
PRINT "   Office (386) 663-1257 ext. 1375 - michellecdjr@gmail.com"
PRINT
COLOR 8, 1
PRINT "   Not affiliated with Stellantis. Jeep is a trademark of FCA US LLC."
COLOR 7, 0
END

QuizData:
@@DATA@@

SUB Banner
  COLOR 10, 1
  PRINT
  PRINT "   __     __   _           _         _   _ _     _                   "
  PRINT "   \ \   / /__| |_   _ ___(_) __ _  | | | (_)___| |_ ___  _ __ _   _ "
  PRINT "    \ \ / / _ \ | | | / __| |/ _` | | |_| | / __| __/ _ \| '__| | | |"
  PRINT "     \ V / (_) | | |_| \__ \ | (_| | |  _  | \__ \ || (_) | |  | |_| |"
  PRINT "      \_/ \___/|_|\__,_|___/_|\__,_| |_| |_|_|___/\__\___/|_|   \__, |"
  PRINT "                                                                 |___/ "
  COLOR 14, 1
  PRINT "                    Q U I Z   -   by Jeep Michelle, NSB FL"
END SUB

SUB WaitKey
  DO WHILE INKEY$ <> "": LOOP
  DO
    SLEEP 1
  LOOP WHILE INKEY$ = ""
END SUB

SUB WrapPrint (t$, fg%)
  COLOR fg%, 1
  s$ = t$
  DO WHILE LEN(s$) > 74
    p% = 74
    DO WHILE MID$(s$, p%, 1) <> " " AND p% > 1
      p% = p% - 1
    LOOP
    PRINT "   "; LEFT$(s$, p% - 1)
    s$ = MID$(s$, p% + 1)
  LOOP
  PRINT "   "; s$
END SUB
'''.replace('@@N@@',str(N)).replace('@@DATA@@','\n'.join(data))
open("VOLUSIA.BAS","w",newline="\r\n").write(bas)
json.dump([{"q":q,"o":o,"a":"ABCD".index(a),"f":f} for q,o,a,f in Q], open("questions.json","w"), indent=1)
print("built", len(bas.splitlines()), "lines")
