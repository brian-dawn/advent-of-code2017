module Problem07 where
import           Control.Applicative
import           Control.Monad
import           Data.Either
import           Data.Foldable
import           Data.List
import qualified Data.Map.Strict     as Map
import           Data.Ord
import qualified Data.Set            as Set

type Weight = Int
type Name = String
data Program = Program {name    :: Name
                       , weight :: Weight
                       , above  :: [Name]
                       } deriving (Eq, Show)

butLast :: [a] -> [a]
butLast xs = take (length xs - 1) xs

parseWeight :: String -> Weight
parseWeight = read . butLast . drop 1

parseNames :: [String] -> [Name]
parseNames names = (map butLast $ butLast names) ++ drop (length names - 1) names

parseLine :: String -> Program
parseLine input = Program name weight subPrograms
  where
    parsed = words input
    name = parsed !! 0
    weight = parseWeight $ parsed !! 1
    subPrograms = parseNames $ drop 3 parsed

solve :: [Program] -> Set.Set Name
solve programs = Set.difference (Set.fromList (map name programs)) allSubPrograms
  where
    allSubPrograms = foldr Set.union Set.empty $ map (Set.fromList . above) programs

data Tree = Tree Weight [Tree] deriving Show
type ProgramDB = Map.Map Name Program
buildProgramDB :: [Program] -> ProgramDB
buildProgramDB = foldr (\ program -> Map.insert (name program) program) Map.empty

buildTree  :: ProgramDB -> Name -> Tree
buildTree programDB rootName = if null (above rootProgram)
                               then Tree (weight rootProgram) []
                               else Tree (weight rootProgram) (map (\n -> buildTree programDB n) (above rootProgram))
  where
    rootProgram = case Map.lookup rootName programDB of
                    Just program -> program
                    -- We know this won't get hit so short circuit.
                    Nothing      -> Program "" 0 []

same :: Eq a => [a] -> Bool
same []     = True
same (x:xs) = null $ filter (/=x) xs


mostPopular :: Ord a => [a] -> a
mostPopular = head
            . concat
            . reverse
            . sortBy (comparing length)
            . group
            . sort

firstUnique (x:xs)
  | elem x xs = firstUnique (filter (/= x) xs)
  | otherwise = Just x
firstUnique [] = Nothing

findImbalanced :: Tree -> (Weight, Either Weight Weight)
findImbalanced (Tree weight []) = (0, Right weight)
findImbalanced (Tree weight children) = if null lefts
                                        then if same childWeights
                                                -- Return our weight
                                             then (weight, (+weight) <$> sum <$> sequence childWeights)
                                             else ( weight
                                                  , do
                                                      tuPop <- mostPopular childWeights :: Either Weight Weight
                                                      let found = firstUnique childWeights :: Maybe (Either Weight Weight)
                                                      let (badWeight, badChildrenWeight) =
                                                            case firstUnique childWeights of
                                                              Just found -> head $ filter ((==found) . snd) childTuples
                                                              -- Can't happen.
                                                              Nothing -> (0, Left 0)
                                                      badChildrenWeightUnboxed <- badChildrenWeight
                                                      Left $ badWeight - (badChildrenWeightUnboxed - tuPop))

                                        -- We know there's only 1 bad one.
                                        else (weight, head $ lefts)

  where
    childTuples = map findImbalanced children
    childWeights = map snd childTuples
    lefts = (filter isLeft childWeights)

answer :: IO()
answer = do
  putStrLn "Problem07"
  input <- readFile "input/Problem07.input"
  let programs = map parseLine $ lines input
  let rootNode = head $ Set.elems $ solve programs
  putStrLn $ rootNode

  let programDB = buildProgramDB programs
  let answer = snd $ findImbalanced $ buildTree programDB rootNode
  case answer of
    Right a -> putStrLn "Failed to find :("
    Left a  -> print a

