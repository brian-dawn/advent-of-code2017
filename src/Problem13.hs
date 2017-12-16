module Problem13 where

import           Control.Monad

-- movement size = concat $ repeat $ [0..size] ++ (reverse [1..size-1])

atTop :: Integer -> Integer -> Bool
atTop size n = n `mod` ((size-1) * 2) == 0


type Size = Integer
type Distance = Integer

solve :: Integer -> [(Distance, Size)] -> Integer
solve delay input = foldr (\(distance, size) severity ->
                             if atTop size $ distance + delay
                             then severity + distance * size + delay -- cheaty way of ensuring getting caught at 0
                             else severity)
                    0
                    input

solve2 delay input =
  if solve delay input == 0
  then delay
  else solve2 (delay+1) input

answer = do
  putStrLn "Problem13"
  file <- readFile "input/Problem13.input"

  let wrds = map words $ lines file :: [[String]]
  let parsed = map (\(a:b:_) -> ((read $ init a), read b)) wrds :: [(Distance, Size)]
  print $ solve 0 parsed
  print $ solve2 0 parsed
