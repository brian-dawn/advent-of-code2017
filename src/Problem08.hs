module Problem08 where

import           Control.Applicative
import           Control.Monad
import           Data.Char
import Data.List
import Data.Ord
import qualified Data.Map.Strict as Map
import           Text.ParserCombinators.ReadP

data Operation = Inc | Dec deriving (Eq, Show)
data Operator = EqualTo
              | NotEqualTo
              | LessThan
              | GreaterThan
              | GreaterThanEqual
              | LessThanEqual deriving (Eq, Show)

type Variable = String

digit :: ReadP Char
digit = satisfy isDigit

negative :: ReadP Char
negative = satisfy (=='-')

number :: ReadP Int
number = do
    sign <- option ' ' negative
    digits <- many1 digit
    return $ read $ sign:digits

operation :: ReadP Operation
operation = do
    val <- string "dec" <|> string "inc"
    return $ case val of
            "dec" -> Dec
            "inc" -> Inc

operatorMapping :: [(String, Operator)]
operatorMapping = [ ("==", EqualTo)
                  , ("!=", NotEqualTo)]



op1 = string "==" >> return EqualTo
op2 = string "!=" >> return NotEqualTo
op3 = string "<"  >> return LessThan
op4 = string "<=" >> return LessThanEqual
op5 = string ">"  >> return GreaterThan
op6 = string ">=" >> return GreaterThanEqual

operator :: ReadP Operator
operator = op1
       <|> op2
       <|> op3
       <|> op4
       <|> op5
       <|> op6

variable :: ReadP Variable
variable = munch1 (\c -> c >= 'a' && c <= 'z'
                      || c >= 'A' && c <= 'Z')


data Line = Line Variable Operation Int Variable Operator Int deriving Show
type Program = [Line]

parseLine :: ReadP Line
parseLine = do
  var1        <- variable
  skipSpaces
  operation   <- operation
  skipSpaces
  amount      <- number
  skipSpaces
  string "if"
  skipSpaces
  var2        <- variable
  skipSpaces
  op          <- operator
  skipSpaces
  checkAmount <- number
  return $ Line var1 operation amount var2 op checkAmount

readProgram :: String -> Program
readProgram = map ( fst
                  . head
                  . sortBy (comparing snd)
                  . readP_to_S parseLine)
              . lines

type State = Map.Map Variable Int

checkCondition :: Ord a => Operator -> a -> a -> Bool
checkCondition NotEqualTo       = (/=)
checkCondition EqualTo          = (==)
checkCondition LessThan         = (<)
checkCondition LessThanEqual    = (<=)
checkCondition GreaterThan      = (>)
checkCondition GreaterThanEqual = (>=)

mutate :: Num a => Operation -> a -> a -> a
mutate Inc = (+)
mutate Dec = (-)

runLine :: Line -> State -> State
runLine (Line varToMutate operation amount condVar operator checkAmount) state =
  if conditionMet then
    Map.insert "highest-register" newestHighest $ Map.insert varToMutate mutation state
  else
    state
  where
    condVarFound = case Map.lookup condVar state of
                     Just n -> n
                     Nothing -> 0
    conditionMet = checkCondition operator condVarFound checkAmount

    mutateVarFound = case Map.lookup varToMutate state of
                       Just n -> n
                       Nothing -> 0
    mutation = mutate operation mutateVarFound amount

    highestRegister = case Map.lookup "highest-register" state of
                        Just n -> n
                        Nothing -> 0
    newestHighest = if mutation > highestRegister then mutation else highestRegister

runProgram :: Program -> State
runProgram = foldr runLine Map.empty . reverse

answer :: IO()
answer = do
  putStrLn "Problem08"
  file <- readFile "input/Problem08.input"
  print $ maximum $ map snd $ Map.toList $ runProgram $ readProgram file
  case Map.lookup "highest-register" $ runProgram $ readProgram file of
    Just n -> print n
    Nothing -> putStrLn "No highest register has been set"





