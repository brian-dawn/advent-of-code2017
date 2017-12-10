module Problem07 where

import Data.Ord
import Data.Function (on)
import Data.List
import Data.Tree
import Data.Char
import Data.Maybe (fromJust)

import qualified Data.Set as S
import qualified Data.Map as M

parseLine :: String -> (String, (Int, S.Set String))
parseLine s = case words s of
  (name:weight:[]) -> (name, (read weight, S.empty))
  (name:weight:_:children) -> (name, (read weight, S.fromList $ map (filter isAlpha) children))

parse :: String -> M.Map String (Int, S.Set String)
parse = M.fromList . (map parseLine) . lines

findRoot :: M.Map String (Int, S.Set String) -> String
findRoot m = S.elemAt 0 $ all S.\\ children where
  all      = M.keysSet m
  children = S.unions $ (map snd) $ M.elems m

children :: String -> M.Map String (Int, S.Set String) -> [String]
children name m = S.toList $ snd . fromJust $ M.lookup name m

weight :: String -> M.Map String (Int, S.Set String) -> Int
weight name m = fst . fromJust $ M.lookup name m

buildTree :: M.Map String (Int, S.Set String) -> Tree (String, Int)
buildTree m = unfoldTree f root where
  root = findRoot m
  f name = ((name, weight name m), children name m)

sumTree :: Tree (String, Int) -> Int
sumTree = sum . (fmap snd)

sumSubtrees :: Tree (String, Int) -> Tree (String, (Int, Int))
sumSubtrees = unfoldTree f where
  f tree@(Node (name, weight) children) = ((name, (weight, sumTree tree)), children)

listOfChildren :: Tree (String, (Int, Int)) -> [[(Int, Int)]]
listOfChildren (Node (name, weight) []) = []
listOfChildren (Node (name, weight) children) = [map labelWeight children] ++ (concatMap listOfChildren children)

labelWeight = snd . rootLabel

same :: [Int] -> Bool
same = (== 1) . length . S.fromList

findChildren :: String -> [[(Int, Int)]]
findChildren = listOfChildren . sumSubtrees . buildTree . parse

differentSubtreeWeights :: [(Int, Int)] -> Bool
differentSubtreeWeights = not . same . (map snd)

firstUnbalancedLevel :: String -> [(Int, Int)]
firstUnbalancedLevel = last
  . (filter differentSubtreeWeights)
  . findChildren

reorderUnbalancedLevel :: [(Int, Int)] -> [[(Int, Int)]]
reorderUnbalancedLevel = sort
  . (groupBy ((==) `on` snd))
  . (sortBy (comparing snd))

findExpectedWeight :: [[(Int, Int)]] -> Int
findExpectedWeight x = actualDisk + (expectedSubtree - actualSubtree) where
  actualDisk = (fst . head . head) x
  actualSubtree = (snd . head . head) x
  expectedSubtree = (snd . head . (head . tail)) x

solve :: String -> Int
solve = findExpectedWeight . reorderUnbalancedLevel . firstUnbalancedLevel

example = "pbga (66)\n\
          \xhth (57)\n\
          \ebii (61)\n\
          \havc (66)\n\
          \ktlj (57)\n\
          \fwft (72) -> ktlj, cntj, xhth\n\
          \qoyq (66)\n\
          \padx (45) -> pbga, havc, qoyq\n\
          \tknk (41) -> ugml, padx, fwft\n\
          \jptl (61)\n\
          \ugml (68) -> gyxo, ebii, jptl\n\
          \gyxo (61)\n\
          \cntj (57)"

partOneAnswer :: String -> String
partOneAnswer = findRoot . parse

partTwoAnswer :: String -> Int
partTwoAnswer = solve
