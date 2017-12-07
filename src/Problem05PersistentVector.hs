module Problem05PersistentVector where

import Data.Vector.Persistent (Vector, fromList, index, (//))
import Data.Maybe

parse :: String -> [Int]
parse = map read . lines

data Program = Program { instructions :: Vector Int, programCounter :: Int }

step :: Program -> (Int -> Int) -> Program
step program modifyOffset = Program nextInstructions nextProgramCounter
  where currentProgramCounter = programCounter program
        currentInstructions   = instructions program
        steps                 = fromJust $ currentInstructions `index` currentProgramCounter -- unsafe fromJust
        nextProgramCounter    = currentProgramCounter + steps
        nextInstructions      = (instructions program) // [(currentProgramCounter, modifyOffset steps)]

completed :: Program -> Bool
completed program = programCounter program >= length (instructions program) || programCounter program < 0

run :: Program -> (Int -> Int) -> Int
run program modifyOffset = runHelper program 0
  where runHelper program count = if completed program
                                  then count
                                  else runHelper (step program modifyOffset) (count + 1)

partOneAnswer :: String -> Int
partOneAnswer input = run (Program (fromList (parse input)) 0) (+ 1)

partTwoAnswer :: String -> Int
partTwoAnswer input = run (Program (fromList (parse input)) 0) (\x -> if x >= 3 then x - 1 else x + 1)

-- stack exec advent-of-code2017  775.85s user 13.30s system 99% cpu 13:13.14 total.
