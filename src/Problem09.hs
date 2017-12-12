module Problem09 where

import Data.Maybe (fromJust)
import Data.Text (strip, unpack, pack)
import Control.Applicative (liftA2, (<|>))
import Text.ParserCombinators.ReadP

combine :: a -> a -> [a]
combine x y = [x] ++ [y]

garbageOpen :: ReadP String
garbageOpen = string "<"

garbageClose :: ReadP String
garbageClose = string ">"

notCancelledGarbage :: ReadP String
notCancelledGarbage = munch1 (\c -> c /= '>' && c /= '!')

cancelledGarbage :: ReadP String
cancelledGarbage = char '!' >> get >> return ""

garbageContents :: ReadP String
garbageContents = concat <$> (many $ notCancelledGarbage +++ cancelledGarbage)

(++++) :: ReadP String -> ReadP String -> ReadP String
(++++) = liftA2 (++)

garbage :: ReadP String
garbage = garbageOpen ++++ garbageContents ++++ garbageClose

groupOpen = string "{"
groupClose = string "}"

ignoredGarbage :: ReadP String
ignoredGarbage = garbage >> return ""

group :: ReadP String
group = do
  open <- groupOpen
  groups <- sepBy (group +++ ignoredGarbage) (char ',')
  close <- groupClose
  return $ open ++ (concat groups) ++ close

-- shouldn't need to allow ambiguous parses, but the optional things in part two were throwing me off
parseMaybe :: ReadP a -> String -> Maybe a
parseMaybe parser string = case filter complete parses of
  [(result, "")] -> Just result
  otherwise      -> Nothing
  where
    parses = readP_to_S parser string
    complete (_,"") = True
    complete (_,_) = False

-- partial :/
scoreGroups :: String -> Int
scoreGroups groups = score groups [] 0 where
  score [] [] currentScore = currentScore
  score [] (_:_)  currentScore = error "Unbalanced"
  score (x:xs) stack currentScore = if x == '{'
                                    then score xs (x:stack) currentScore
                                    else score xs (tail stack) (currentScore + (length stack))

partOneAnswer :: String -> Int
partOneAnswer input = fromJust $ scoreGroups <$> (parseMaybe group) (unpack . strip . pack $ input)

groupChars :: ReadP String
groupChars = munch (\c -> c == '}' || c == '{' || c == ',')

ignoreCancelled :: ReadP String
ignoreCancelled = cancelledGarbage >> return ""

countGarbage :: ReadP Int
countGarbage = do
  garbageOpen
  content <- garbageContents
  garbageClose
  return $ length content

sumGarbage :: ReadP Int
sumGarbage = do
  groupChars
  garbageCounts <- sepBy1 countGarbage groupChars
  groupChars
  return $ sum garbageCounts

--partTwoAnswer :: String -> Int
partTwoAnswer =  fromJust . (parseMaybe sumGarbage) . (unpack . strip . pack)

garbageExamples = ["<>", "<random characters>", "<<<<>", "<{!>}>", "<!!>", "<!!!>>", "<{o\"i!a,<{i<a>"]
groupExamples = [("{}", 1),
                 ("{{{}}}", 6),
                 ("{{},{}}", 5),
                 ("{{{},{},{{}}}}", 16),
                 ("{<a>,<a>,<a>,<a>}", 1),
                 ("{{<ab>},{<ab>},{<ab>},{<ab>}}", 9),
                 ("{{<!!>},{<!!>},{<!!>},{<!!>}}", 9),
                 ("{{<a!>},{<a!>},{<a!>},{<ab>}}", 3)]

test examples = pure expected == actual where
  (input, expected) = unzip examples
  actual = (map scoreGroups) <$> (sequence $ map (parseMaybe group) input)

test2 examples = pure expected == actual where
  (input, expected) = unzip examples
  actual = sequence $ map (parseMaybe sumGarbage) input

answer1 = test groupExamples
answer2 = test2 [("{<>}", 0),
                 ("{<random characters>}", 17),
                 ("{<<<<>}", 3),
                 ("{<{!>}>}", 2),
                 ("{<!!>}", 0),
                 ("{<!!!>>}", 0),
                 ("{<{o\"i!a,<{i<a>}", 10)]
