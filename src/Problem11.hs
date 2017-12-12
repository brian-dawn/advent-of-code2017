{-# LANGUAGE OverloadedStrings #-}

module Problem11 where

import qualified Data.Text as T

--    +y   -z
--      \ /
--  -x -   - +x
--      / \
--    +z   -y
-- hex location in cube coordinates
data Hex = Hex { x :: Int
               , y :: Int
               , z :: Int
               }

distance :: Hex -> Hex -> Int
distance a b = maximum [abs (x a - x b),
                        abs (y a - y a),
                        abs (z a - z b)]

distanceFromOrigin :: Hex -> Int
distanceFromOrigin = distance $ Hex 0 0 0

parse :: String -> [String]
parse = (map T.unpack) . (T.splitOn ",") . T.strip . T.pack

direction :: String -> Hex
direction t = case t of
  "n"  -> Hex 0 1 (-1)
  "ne" -> Hex 1 0 (-1)
  "se" -> Hex 1 (-1) 0
  "s"  -> Hex 0 (-1) 1
  "sw" -> Hex (-1) 0 1
  "nw" -> Hex (-1) 1 0
  otherwise -> error "No parse"

addHex :: Hex -> Hex -> Hex
addHex a b = Hex (x a + x b)
                 (y a + y b)
                 (z a + z b)

partOneAnswer :: String -> Int
partOneAnswer = distanceFromOrigin . (foldl addHex (Hex 0 0 0)) . (map direction) . parse

partTwoAnswer :: String -> Int
partTwoAnswer = maximum . (map distanceFromOrigin) . (scanl addHex (Hex 0 0 0)) . (map direction) . parse


-- examples = [("ne,ne,ne", 3),
--             ("ne,ne,sw,sw", 0),
--             ("ne,ne,s,s", 2),
--             ("se,sw,se,sw,sw", 3)]

-- test = actual == expected where
--   actual = map partOneAnswer input
--   (input, expected) = unzip examples
