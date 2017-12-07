module Problem05 where

import Data.Vector (Vector, fromList, (!), (//))

parse :: String -> [Int]
parse = map read . lines

data Program = Program { instructions :: Vector Int, index :: Int }

step :: Program -> (Int -> Int) -> Program
step program modifyOffset = Program nextInstructions nextIndex
  where currentIndex        = index program
        currentInstructions = instructions program
        steps               = currentInstructions ! currentIndex
        nextIndex           = currentIndex + steps
        nextInstructions    = (instructions program) // [(currentIndex, modifyOffset steps)]

completed :: Program -> Bool
completed program = index program >= length (instructions program) || index program < 0

run :: Program -> (Int -> Int) -> Int
run program modifyOffset = runHelper program 0
  where runHelper program count = if completed program
                                  then count
                                  else runHelper (step program modifyOffset) (count + 1)

partOneAnswer :: String -> Int
partOneAnswer input = run (Program (fromList (parse input)) 0) (+ 1)

partTwoAnswer :: String -> Int
partTwoAnswer input = run (Program (fromList (parse input)) 0) (\x -> if x >= 3 then x - 1 else x + 1)

-- try with mutable vectors tomorrow

-- stack exec advent-of-code2017  31.92s user 0.69s system 99% cpu 32.692 total
