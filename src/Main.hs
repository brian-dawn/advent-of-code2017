module Main where

import qualified Problem01 as P01

main :: IO ()
main = do
  putStrLn "Solutions: "
  putStrLn "Problem 1:"
  putStrLn $ "Part 1: " ++ P01.partOneAnswer
  putStrLn $ "Part 2: " ++ P01.partTwoAnswer
