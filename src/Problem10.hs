module Problem10 where

import qualified Data.Bits             as Bits
import qualified Data.ByteString.Char8 as Byte
import           Data.Char
import           Data.List
import           Data.Word
import           Numeric               (showHex, showIntAtBase)

twist :: [Word8] -> Int -> Int -> [Int] -> (Int, Int, [Word8])
twist xs position skipSize [] = (position, skipSize, xs)
twist xs position skipSize (len:lengths) =
  twist newXs newPosition newSkipSize lengths
  where
    xsLen = length xs
    newPosition = position + len + skipSize
    newSkipSize = skipSize + 1

    p = position `mod` xsLen
    rotated = rotate p xs
    newXs = rotate (xsLen-p) $ (reverse $ take len rotated) ++ drop len rotated

rotate :: Int -> [a] -> [a]
rotate _ [] = []
rotate n xs = zipWith const (drop n (cycle xs)) xs

input :: [Int]
input = [230,1,2,221,97,252,168,169,57,99,0,254,181,255,235,167]

input2 = "230,1,2,221,97,252,168,169,57,99,0,254,181,255,235,167"

solve :: [Int]
solve = map fromIntegral result
  where
    (_,_,result) = twist (map fromIntegral [0..255]) 0 0 input

chunks :: Int -> [a] -> [[a]]
chunks _ [] = []
chunks n xs =
    let (ys, zs) = splitAt n xs
    in  ys : chunks n zs

combine :: [Word8] -> Word8
combine = foldr1 Bits.xor

wordToHex :: Word8 -> String
wordToHex word =
  if length s == 1
  then "0" ++ s
  else s
  where
    s = showIntAtBase 16 intToDigit word ""

solve2 :: [Int] -> String
solve2 lengths = foldr1 (++) $ map wordToHex $ map combine groups
  where
    ls = lengths ++ [17, 31, 73, 47, 23]
    run (position, skipSize, xs) = twist xs position skipSize (map fromIntegral ls)
    (_, _, result) = head $ reverse $ take 65 $ iterate run (0, 0, [0..255])
    groups = chunks 16 result :: [[Word8]]

convertToAscii :: [Char] -> [Int]
convertToAscii = map fromEnum

answer = do
  putStrLn "Problem10"
  let (a:b:_) = solve
  print $ a * b
  putStrLn $ solve2 $ convertToAscii input2

