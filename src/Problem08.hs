module Problem08 where

import Data.Map hiding (map, foldl)

example :: String
example = "b inc 5 if a > 1\n\
          \a inc 1 if b < 5\n\
          \c dec -10 if a >= 1\n\
          \c inc -20 if c == 10"

type Register = String
type Amount = Int

data Condition = Condition { reg :: Register
                           , comparison :: Int -> Int -> Bool
                           , target :: Amount }

data Expr = Expr { register :: Register
                 , operation :: Int -> Int -> Int
                 , amount :: Amount
                 , condition :: Condition }

type ProgramState = Map Register Amount

eval :: ProgramState -> Expr -> ProgramState
eval state exp = if (satisfied c state)
                 then adjust (\x -> op x amnt) reg state
                 else state where
  c    = condition exp
  amnt = amount exp
  op   = operation exp
  reg  = register exp

satisfied :: Condition -> ProgramState -> Bool
satisfied cond state = compare a b where
  compare = comparison cond
  a       = findWithDefault 0 (reg cond) state
  b       = target cond

parseLine :: String -> Expr
parseLine line = Expr { register = r
                      , operation = case op of
                          "inc" -> (+)
                          "dec" -> (-)
                      , amount = read amt
                      , condition = Condition { reg = condReg
                                              , comparison = case cmp of
                                                  ">"  -> (>)
                                                  "<"  -> (<)
                                                  ">=" -> (>=)
                                                  "<=" -> (<=)
                                                  "==" -> (==)
                                                  "!=" -> (/=)
                                              , target = read t }
                        } where
  (r:op:amt:_:condReg:cmp:t:[]) = words line

readInstructions :: String -> [Expr]
readInstructions = (map parseLine) . lines

initializeState :: [Expr] -> ProgramState
initializeState exps = fromList $ zip (map register exps) (repeat 0)

parseAndRun :: String -> ProgramState
parseAndRun s = foldl eval state instructions where
  instructions = readInstructions s
  state        = initializeState instructions

partOneAnswer :: String -> Int
partOneAnswer = maximum . elems . parseAndRun

-- part 2

accumulator :: (ProgramState, Amount) -> Expr -> (ProgramState, Amount)
accumulator (state, max) exp = (newState, if newMax > max
                                          then newMax
                                          else max) where
  newState = eval state exp
  newMax   = maximum . elems $ newState

partTwoAnswer :: String -> Int
partTwoAnswer s = snd $ foldl accumulator (state,0) instructions where
  instructions = readInstructions s
  state        = initializeState instructions
