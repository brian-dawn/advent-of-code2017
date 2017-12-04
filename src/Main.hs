module Main where

import qualified Problem01 as P01
import qualified Problem02 as P02

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
