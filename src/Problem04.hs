module Problem04 where

import           Data.List
import           Data.Set  (Set, fromList)

isValid :: (String -> String) -> String -> Bool
isValid xformFn phrase = length ws == length asSet
    where
        ws = words phrase
        asSet = fromList $ map xformFn ws :: Set String


solve :: (String -> Bool) -> String -> Int
solve validFn file = length $ filter (not . null) $ filter validFn $ lines file


answer :: IO()
answer = do
    putStrLn "Problem04"
    file <- readFile "input/Problem04.input"
    print $ solve (isValid id) file
    print $ solve (isValid sort) file

