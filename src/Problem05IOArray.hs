module Problem05IOArray where

import Data.Array.IO
import Data.Array.MArray

parse :: String -> [Int]
parse = map read . lines

data Program = Program { instructions :: IOArray Int Int, programCounter :: Int }

step :: Program -> (Int -> Int) -> IO (Program)
step program f = do
  steps <- currentValue program
  writeArray currentInstructions currentProgramCounter (f steps)
  return $ Program currentInstructions (currentProgramCounter + steps)
  where currentInstructions   = (instructions program)
        currentProgramCounter = (programCounter program)

currentValue :: Program -> IO (Int)
currentValue program = readArray (instructions program) (programCounter program)

completed :: Program -> IO (Bool)
completed program = do
  max <- size (instructions program)
  return $ programCounter program >= max || programCounter program < 0

run :: Program -> (Int -> Int) -> IO (Int)
run program f = runHelper program 0
  where runHelper program count = do
          done <- completed program
          if done
            then return count
            else do
            next <- (step program f)
            runHelper next (count + 1)

makeArray :: [Int] -> IO (IOArray Int Int)
makeArray list = newListArray (0, (length list) - 1) list

size :: IOArray Int Int -> IO (Int)
size array = snd <$> getBounds array

partOneAnswer :: String -> IO (Int)
partOneAnswer input = do
  i <- makeArray (parse input)
  run (Program i 0) (+ 1)

partTwoAnswer :: String -> IO (Int)
partTwoAnswer input = do
  i <- makeArray (parse input)
  run (Program i 0) (\x -> if x >= 3 then x - 1 else x + 1)

-- stack exec advent-of-code2017  1.61s user 0.14s system 100% cpu 1.745 total
