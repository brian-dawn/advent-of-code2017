module Problem04 where

import Data.List
import Data.Set (Set)
import qualified Data.Set as Set

splitInput :: String -> [[String]]
splitInput = (map words) . lines

unique :: Ord a => [a] -> Bool
unique list = length set == length list
  where set = Set.fromList list

countValidPassphrases :: String -> Int
countValidPassphrases = length
  . filter id
  . map unique
  . splitInput

partOneAnswer = countValidPassphrases

-- part 2

countValidPassphrases2 :: String -> Int
countValidPassphrases2 = length
  . filter id
  . map unique
  . map (map sort) -- lol don't need bags, just sort the strings
  . splitInput

partTwoAnswer = countValidPassphrases2
