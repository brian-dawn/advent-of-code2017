module Problem06 where

import           Data.List
import qualified Data.Set  as Set
input :: String
input = "11 11 13 7 0 15 5 5 4 4 1 1 7 1 15 11"

type Bank = [Int]

parsed :: Bank
parsed = map read $ words input

distribute :: Bank -> Int -> Int -> Bank
distribute bank 0          _     = bank
distribute bank blocksLeft index = distribute (before ++ (middle+1:after))
                                              (blocksLeft-1)
                                              (index+1)
  where
    index' = index `mod` length bank
    before = take index' bank
    middle = bank !! index'
    after = drop (index'+1) bank

unbox :: Maybe Int -> Int
unbox m = case m of
  Just a  -> a
  Nothing -> 0

unsafeFindIndex :: (a-> Bool) -> [a] -> Int
unsafeFindIndex f xs = unbox $ (findIndex f xs)

step :: Bank -> Bank
step bank = distribute (before ++ 0:after) highest startIndex
  where
    highest = maximum bank
    -- we know we'll find `highest` so just unsafe find to avoid the maybe.
    startIndex = unsafeFindIndex (==highest) bank + 1
    after = drop startIndex bank
    before = take (startIndex - 1) bank

steps :: Bank -> [Bank]
steps = iterate step

findFirstDup :: [Bank] -> Set.Set Bank -> Int -> Int
findFirstDup (bank:banks) set n = if Set.member bank set then n else findFirstDup banks (Set.insert bank set) (n+1)

solve :: Bank -> Int
solve bank = findFirstDup (steps bank) Set.empty 0

solve2 bank = solve $ steps bank !! startIndex
  where
    startIndex = solve bank

answer = do
  putStrLn "Problem06"
  print $ solve parsed
  print $ solve2 parsed
