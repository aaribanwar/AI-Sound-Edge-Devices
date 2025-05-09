// routes/users.js
import express from "express";
import {
  getUsers,
  createUser,
  getUser,
  updateUser,
  deleteUser
} from "../controllers/userController.js";

const router = express.Router();

router.get("/", getUsers);
router.post("/", createUser);
router.get("/:id", getUser);
router.put("/:id", updateUser);
router.delete("/:id", deleteUser);

export default router;
