{-# LANGUAGE OverloadedStrings #-}
module Problem09 where

import           Control.Applicative
import           Control.Monad
import           Data.Char
import           Data.List

import           Text.ParserCombinators.ReadP

data Token = Garbage Int
           | Group [Token] deriving Show

parseBang :: ReadP (Maybe Char)
parseBang = char '!' >> get >> return Nothing

parseChar :: ReadP (Maybe Char)
parseChar = do
  c <- get
  return $ Just c

parseGarbage :: ReadP Token
parseGarbage = do
  char '<'
  let middle = parseBang <++ parseChar
  chars <- manyTill middle $ char '>'

  return $ Garbage $ length $ filter (/=Nothing) chars

parseGroup :: ReadP Token
parseGroup = do
  char '{'
  elems <- sepBy (choice [parseGroup, parseGarbage]) $ char ','
  char '}'
  return $ Group elems

countGroups :: Int -> Token -> Int
countGroups n (Garbage _) = 0
countGroups n (Group []) = n
countGroups n (Group tokens) = n + (foldr (+) 0 $ map (countGroups (n+1)) tokens)

countChars :: Token -> Int
countChars (Garbage count) = count
countChars (Group [])      = 0
countChars (Group tokens)  = (foldr (+) 0 $ map countChars tokens)

answer :: IO()
answer = do
  putStrLn "Problem09"
  file <- readFile "input/Problem09.input"
  print $ countGroups 1 $ fst $ head $ readP_to_S parseGroup file
  print $ countChars $ fst $ head $ readP_to_S parseGroup file

