module Main where

import qualified Problem01 as P01
import qualified Problem02 as P02
import qualified Problem03 as P03
import qualified Problem04 as P04

-- import qualified Problem05 as P05
-- import qualified Problem05PersistentVector as P05
import qualified Problem05IOArray as P05

import qualified Problem06 as P06

main :: IO ()
main = do
  putStrLn "Solutions: "
  putStrLn "Problem 1:"
  putStrLn $ "\tPart 1: " ++ P01.partOneAnswer
  putStrLn $ "\tPart 2: " ++ P01.partTwoAnswer

  putStrLn "Problem 2:"
  input <- (readFile "./input/problem02.txt")
  putStrLn $ "\tPart 1: " ++ P02.partOneAnswer input
  putStrLn $ "\tPart 2: " ++ P02.partTwoAnswer input

  putStrLn "Problem 3:"
  putStrLn $ "\tPart 1: " ++ P03.partOneAnswer
  p3 <- P03.partTwoAnswer
  putStrLn $ "\tPart 2: " ++ p3

  putStrLn "Problem 4:"
  problem4 <- (readFile "./input/problem04.txt")
  putStrLn $ "\tPart 1: " ++ (show $ P04.partOneAnswer problem4)
  putStrLn $ "\tPart 2: " ++ (show $ P04.partTwoAnswer problem4)

  putStrLn "Problem 5:"
  problem5 <- (readFile "./input/problem05.txt")

  -- putStrLn $ "\tPart 1: " ++ (show $ P05.partOneAnswer problem5)
  -- putStrLn $ "\tPart 1: " ++ (show $ P05.partTwoAnswer problem5)

  p5p1 <- P05.partOneAnswer problem5
  putStrLn $ "\tPart 1: " ++ (show $ p5p1)
  p5p2 <- P05.partTwoAnswer problem5
  putStrLn $ "\tPart 2: " ++ (show $ p5p2)

  putStrLn "Problem 6:"
  problem6 <- (readFile "./input/problem06.txt")
  putStrLn $ "\tPart 1: " ++ (show $ P06.partOneAnswer problem6)
  putStrLn $ "\tPart 1: " ++ (show $ P06.partTwoAnswer problem6)
