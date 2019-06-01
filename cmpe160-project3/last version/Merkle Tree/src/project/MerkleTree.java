package project;

import util.HashGeneration;

import java.io.File;
import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.util.*;

public class MerkleTree {
    private ArrayList<String> corruptPaths;
    private String path;
    private Node root;
    private ArrayList<Stack<String>> errorChunks;

    public MerkleTree(String path) throws IOException, NoSuchAlgorithmException {
        this.path = path;
        Scanner reader = new Scanner(new File(path));
        Queue<String> chunkPaths = new LinkedList<>();
        root = new Node("");
        while (reader.hasNext()) {
            chunkPaths.add(reader.next());
        }
        reader.close();
        int level = 0;
        if (chunkPaths.size() == 0)
            level = 0;
        else if (chunkPaths.size() == 1)
            level = 1;
        else
            level = (int) Math.ceil(Math.log(chunkPaths.size()) / Math.log(2));

        root = createTree(chunkPaths, root, level);
    }

    public Node getRoot() {
        return root;
    }

    private Node createTree(Queue<String> queue, Node node, int level) throws IOException, NoSuchAlgorithmException {
        if (node == null)
            return null;
        else if (queue.isEmpty()) {
            return null;
        } else if (level == 0) {
            String path = queue.poll();
            Node mem = new Node(path);
            mem.hash = HashGeneration.generateSHA256(new File(path));
            return mem;
        } else {
            node.right = new Node("");
            node.left = new Node("");
            node.left = createTree(queue, node.left, level - 1);
            node.right = createTree(queue, node.right, level - 1);
            if (node.right == null)
                node.hash = HashGeneration.generateSHA256(node.left.getData().concat(""));
            else if (node.left == null)
                node.hash = HashGeneration.generateSHA256("".concat(node.right.getData()));
            else
                node.hash = HashGeneration.generateSHA256(node.left.getData().concat(node.right.getData()));

        }
        return node;
    }

    public boolean checkAuthenticity(String path) throws IOException, NoSuchAlgorithmException {
        Scanner read = new Scanner(new File(path));
        return read.nextLine().equals(root.getData());
    }

    public ArrayList<Stack<String>> findCorruptChunks(String path) throws IOException, NoSuchAlgorithmException {
        errorChunks = new ArrayList<>();
        corruptPaths = new ArrayList<>();
        Stack<String> stack = new Stack<>();
        Queue<String> queue = new LinkedList<>();
        MerkleTree metaTree = new MerkleTree(this.path);
        Scanner read = new Scanner(new File(path));
        while (read.hasNext()) {
            queue.add(read.nextLine());
        }
        read.close();
        changeMetaTreeHash(queue, metaTree);
        Node metaRoot = metaTree.getRoot();
        if (!root.getData().equals(metaRoot.getData())) {
            addCorruptChunks(stack, root, metaRoot);
        }

        return errorChunks;

    }

    private void addCorruptChunks(Stack<String> stack, Node treeNode, Node metaNode) {
        if (treeNode == null)
            return;
        else if (treeNode.isLeaf()) {
            stack.add(treeNode.getData());
            errorChunks.add(stack);
            corruptPaths.add(treeNode.path);

        } else if (!treeNode.getData().equals(metaNode.getData())) {
            stack.add(treeNode.getData());
            if (treeNode.left != null && !treeNode.left.getData().equals(metaNode.left.getData()))
                addCorruptChunks(stack, treeNode.left, metaNode.left);
            if (treeNode.right != null && !treeNode.right.getData().equals(metaNode.right.getData()))
                addCorruptChunks(stack, treeNode.right, metaNode.right);
        }
    }

    private void changeMetaTreeHash(Queue<String> queue, MerkleTree metaTree) {
        Queue<Node> nodeQueue = new LinkedList<>();
        Node current;
        if (!queue.isEmpty())
            metaTree.getRoot().hash = queue.poll();
        nodeQueue.add(metaTree.getRoot());
        while (!queue.isEmpty()) {
            if (!nodeQueue.isEmpty()) {
                current = nodeQueue.poll();
                if (current.left != null) {
                    current.left.hash = queue.poll();
                    nodeQueue.add(current.left);
                }
                if (current.right != null) {
                    current.right.hash = queue.poll();
                    nodeQueue.add(current.right);
                }
            }
        }
    }

    public ArrayList<String> getCorruptPaths(String path) throws IOException, NoSuchAlgorithmException {
        findCorruptChunks(path);
        return corruptPaths;

    }
}

