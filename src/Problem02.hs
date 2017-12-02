module Problem02 where

import           Control.Applicative
import           Data.List

lineToNums :: String -> [Int]
lineToNums = map read . words

readTable :: String -> [[Int]]
readTable = map lineToNums . lines

solve :: String -> Int
solve xs = foldl1 (+) $ zipWith (-) maxs mins
    where
        c = readTable xs
        maxs = map maximum c
        mins = map minimum c

findDivisible :: [Int] -> Int
findDivisible xs = finalA `div` finalB
    where
        perms = filter (\(a, b) -> a /= b) $ combinations xs xs
        (finalA, finalB) = head $ dropWhile (\(a, b) -> a `mod` b /= 0) perms

combinations :: [a] -> [b] -> [(a,b)]
combinations a b = (,) <$> a <*> b

solve2 :: String -> Int
solve2 xs = foldl1 (+) $ map findDivisible nums
    where
        nums = readTable xs

answer :: IO()
answer = do
    putStrLn "Problem02"
    file <- readFile "input/Problem02.input"
    print $ solve file
    print $ solve2 file

