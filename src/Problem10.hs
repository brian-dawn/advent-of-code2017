{-# LANGUAGE OverloadedStrings #-}
module Problem10 where

import Text.Printf
import Data.Bits (xor)
import Data.List (unfoldr)
import Data.Char
import Data.Text (Text, strip, pack, unpack, splitOn)
import qualified Data.Vector as V

circularReverseSegment :: Int -> Int -> V.Vector a -> V.Vector a
circularReverseSegment pos len v =
  if len > n || len < 0 then error "Invalid length" else
    if pos + len <= n
    then let
      front = V.slice 0 pos v
      middle = V.slice pos len v
      back = V.slice (pos + len) (n - len - pos) v in
        front V.++ V.reverse middle V.++ back
    else let
      front = V.slice 0 (pos + len - n) v
      middle = V.slice (pos + len - n) (n - len) v
      back = V.slice pos (n - pos) v
      split = n - pos in
        let (newBack, newFront) = V.splitAt split (V.reverse (back V.++ front)) in
          newFront V.++ middle V.++ newBack
  where n = V.length v

-- a little better looking
circularReverseSegment' :: Int -> Int -> V.Vector a -> V.Vector a
circularReverseSegment' pos len v = unrotate reversedAndRotated where
  rotate   vec = let (front, back) = V.splitAt
                                     pos
                                     vec
                 in back V.++ front
  unrotate vec = let (back, front) = V.splitAt
                                     ((length v) - pos)
                                     vec
                 in front V.++ back

  rotated = rotate v
  (chunkToReverse, rest) = V.splitAt len rotated
  reversed = V.reverse chunkToReverse
  reversedAndRotated = reversed V.++ rest

step :: (Int, Int, V.Vector a) -> Int -> (Int, Int, V.Vector a)
step (pos, skip, v) len = ((pos + len + skip) `mod` (V.length v), skip + 1, circularReverseSegment' pos len v)

run :: Int -> Int -> V.Vector Int -> [Int] -> (Int, Int, V.Vector Int)
run pos skip v lengths = foldl step (pos, skip, v) lengths

check :: (Int, Int, V.Vector Int) -> Int
check (_, _, v) = v V.! 0 * v V.! 1

parse :: String -> [Int]
parse = (map (read . unpack)) . (splitOn ("," :: Text)) . strip . pack

partOneAnswer :: String -> Int
partOneAnswer = check . (run 0 0 (V.enumFromN 0 256)) . parse

suffix :: [Int]
suffix = [17, 31, 73, 47, 23]

parse2 :: String -> [Int]
parse2 s = ((map ord) $ unpack $ strip $ pack $ s) ++ suffix

rounds :: [Int] -> (Int, Int, V.Vector Int)
rounds lengths = head $ drop 64 $ iterate round (0, 0, (V.enumFromN 0 256)) where
  round (pos, skip, v) = run pos skip v lengths

sparseHash :: (Int, Int, V.Vector Int) -> V.Vector Int
sparseHash (_,_,v) = v

chunks :: Int -> [Int] -> [[Int]]
chunks n = takeWhile (not . null) . unfoldr (Just . splitAt n)

denseHash :: [[Int]] -> [Int]
denseHash = map (foldl1 xor)

format :: Int -> String
format = printf "%02x"

partTwoAnswer :: String -> String
partTwoAnswer = concat . (map format) . denseHash . (chunks 16) . V.toList . sparseHash . rounds . parse2
