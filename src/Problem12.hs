module Problem12 where

import Data.Char
import Data.Foldable
import Data.Graph
import Data.Tree

parseLine :: String -> (Int, Int, [Int])
parseLine line = (read node,
                  read node,
                  map read $ map (filter isDigit) neighbors)  where
  (node:_:neighbors) = words line

parse :: String -> [(Int, Int, [Int])]
parse = map parseLine . lines

graph :: [(Int, Int, [Int])] -> Graph
graph edgeList = let (g,_,_) = graphFromEdges edgeList in g

partOneAnswer :: String -> Int
partOneAnswer = length . head . (filter (elem 0)) . components . graph . parse

partTwoAnswer = length . components . graph . parse
