module Problem11 where

import           Data.List.Split
import           Math.Geometry.Grid           (Grid, distance, indices,
                                               neighbours)
import           Math.Geometry.Grid.Hexagonal

data Direction = SE | NE | SW | NW | N | S deriving Show

readDirection :: String -> Direction
readDirection "se" = SE
readDirection "ne" = NE
readDirection "sw" = SW
readDirection "nw" = NW
readDirection "s"  = S
readDirection "n"  = N

parse :: String -> [Direction]
parse = map readDirection . splitOn ","

-- rotated to work with `grid`.
walk :: Direction -> (Int, Int) -> (Int, Int)
walk N  (x, y) = (x+1, y-1)
walk S  (x, y) = (x-1, y+1)
walk NE (x, y) = (x+1, y)
walk SE (x, y) = (x, y+1)
walk NW (x, y) = (x, y-1)
walk SW (x, y) = (x-1, y)

origin :: (Int, Int)
origin = (0, 0)

holdBiggest :: HexHexGrid -> (Int, (Int, Int)) -> Direction -> (Int, (Int, Int))
holdBiggest g (biggest, currentPos) val = (newBiggest, newLocation)
  where
    newBiggest = max biggest $ distance g origin currentPos
    newLocation = walk val currentPos

answer = do

  file <- readFile "input/Problem11.input"
  print $ length $ parse file
  let g = hexHexGrid $ length file
  let w = foldl (holdBiggest g) (0, origin) (parse file)
  print $ distance g origin $ snd w
  print $ fst w


