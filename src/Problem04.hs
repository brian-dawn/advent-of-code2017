module Problem04 where

import Data.Set (Set)
import qualified Data.Set as Set

import Data.MultiSet (MultiSet)
import qualified Data.MultiSet as MultiSet

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

wordToBagOfLetters :: String -> MultiSet Char
wordToBagOfLetters = MultiSet.fromList

countValidPassphrases2 :: String -> Int
countValidPassphrases2 = length
  . filter id
  . map unique
  . map (map wordToBagOfLetters)
  . splitInput

partTwoAnswer = countValidPassphrases2
