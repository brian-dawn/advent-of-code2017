module Problem06 where

import Prelude hiding (length)
import Data.Vector hiding (take, drop, foldl, map)

import Data.Map (Map)
import qualified Data.Map as Map

circularIndices :: Vector a -> [Int]
circularIndices v = cycle [0 .. (length v - 1)]

incrementIndex :: Vector Int -> Int -> Vector Int
incrementIndex v i = v // [(i, ((v ! i) + 1))]

maxWithIndex :: Vector Int -> (Int, Int)
maxWithIndex v = (max, i)
  where i   = maxIndex v
        max = v ! i

distribute :: Vector Int -> Vector Int
distribute v = foldl incrementIndex newV idxs
  where (max, i) = maxWithIndex v
        newV = v // [(i, 0)]
        idxs = take max $ drop (i + 1) $ circularIndices v

distributeUntilDuplicate :: Vector Int -> (Int, Int)
distributeUntilDuplicate v = helper v Map.empty 0
  where helper v m n = if Map.member v m
               then (n, Map.findWithDefault 0 v m)
               else helper (distribute v) (Map.insert v n m) (n + 1)

parse :: String -> [Int]
parse = (map read) . words

partOneAnswer :: String -> Int
partOneAnswer = fst . distributeUntilDuplicate . fromList . parse

partTwoAnswer :: String -> Int
partTwoAnswer = (uncurry (-)) . distributeUntilDuplicate . fromList . parse
