from smolagents import CodeAgent, DuckDuckGoSearchTool, Tool, HfApiModel
import os
from dotenv import load_dotenv
class FileReaderTool(Tool):
    name = "file_reader_tool"
    description = """
    This tool will be used by the LLM Agent to read files to help analyze files for its task.
    """
    inputs = {
        "file_location": {
            "type": "string",
            "description": "The location of the file that will be read/analyzed"
        }
    }
    output_type = "string"

    def forward(self,file_location ) -> str:
        with open(file_location, "r") as file:
            return file.read()
        
class FileWriteTool(Tool):
    name = "file_write_tool"
    description = """
    This tool will be used by the LLM Agent to overwrite files if needed for task.
    """
    inputs = {
        "file_location": {
            "type": "string",
            "description": "The location of the file that will be read/analyzed"
        },
        "new_code": {
            "type": "string",
            "description": "This is the code that will overwrite the contents of a file. If file does not exist, it is the new content."
        }
    }
    output_type = "string"

    def forward(self,file_location, new_code) -> str:
        with open(file_location, "w") as file:
            return file.write(new_code)

class FileModifyTool(Tool):
    name = "file_modify_tool"
    description = """
    This tool will be used by the LLM Agent to modify files if needed for task.
    """
    inputs = {
        "file_location": {
            "type": "string",
            "description": "The location of the file that will be read/analyzed"
        },
        "prompt": {
            "type": "string",
            "description": "This is the prompt that the LLM will use to decide how to modify the code."
        }
    }
    output_type = "string"

    def forward(self,file_location, prompt) -> str:
        load_dotenv() 

        HF_TOKEN = os.getenv("HF_TOKEN")

        file_reader_tool = FileReaderTool()
        file_write_tool = FileWriteTool()

        model = HfApiModel("Qwen/Qwen2.5-Coder-32B-Instruct", token=HF_TOKEN)
        coderAgent = CodeAgent(tools=[file_reader_tool, file_write_tool], model=model)

        file_content = file_reader_tool.forward(file_location)

        if not file_content:
            return "Error: File could not be read."

        modified_code = coderAgent.run(f"Modify this code based on the instruction:\n{file_content}\n\n{prompt}")
        if "ERROR" in modified_code:
            return "Modification failed, please refine your request."
        write_result = file_write_tool.forward(file_location, modified_code)
        return "Code updated successfully!" if write_result else "Failed to update code."

        


class FileReplaceTool(Tool):
    name = "file_replace_tool"
    description ="""
    This tool will be used to replace the file in a given location with the provided new file location. This is not used to update files.
    """
    inputs = {
        "target_file_location": {
            "type": "string",
            "description": "the location of the file that will be replaced"
        },
        "new_file_location": {
            "type": "string",
            "description": "the location of the new file to replace target file location"
        }
    }
    output_type = "string"
    def forward(self, target_file_location, new_file_location) -> str:
        import os
        import shutil

        if os.path.exists(new_file_location):
            # Define the destination path for the saved image
        #     # Create the './generatedImages' directory if it doesn't exist
        #     # Copy the image from the temporary location to the desired directory
            shutil.copy(new_file_location, target_file_location)

            return print(f"Image saved to {target_file_location}")
        else:
            return print("Failed to generate an image or the file does not exist.")
        
class GetImageDimensionsTool(Tool):
    name = "get_image_dimensions_tool"
    description= """
    This tool is used to get the width and height of a webp file.
    """
    inputs = {
        "file_location": {
            "type": "string",
            "description": "The location in which the webp file can be located"
        }
    }
    output_type = "object"
    def forward(self, file_location) -> dict:
        from PIL import Image

        with Image.open(file_location) as img:
            width, height = img.size

        return {"width": width, "height": height}

class ProcessFlowIdentifierTool(Tool):
    name = "process_flow_identifier_tool"
    description = """
    This tool will be used to give a set of instructions depending on the purpose of the prompt. This is to aid the LLM in its decision making process.
    """
    inputs = {
        "prompt_objective": {
            "type": "string",
            "description": "This is the objective of the user's original prompt to help identify the steps needed for the llm to take."
        }
    }
    output_type = "string"
    def forward(self, prompt_objective) -> str:
        match prompt_objective:
            case "asset_change":
                instructions = """
                1. Find the webp file assosciated with prompt.
                2. Copy original asset's dimensions using the get_image_dimensions_tool(file_location).
                3. Generate the image using the image_generation_tool(prompt,width,height) and add the width and height as parameters that follows the original file (example: image_generation_tool(prompt"", width=32px, height=32px)).
                4. Download the image and replace the original using the FileUpdateTool tool.
                """
                return instructions
            case "script_change":
                instructions = """
                none yet
                """
                return instructions
            case _:
                instructions = """
                inform user that the instructions where unclear
                """
                return instructions
        

class GitPushTool(Tool):
    name = "git_push_tool"
    description = """
    This tool will be triggered to create a new branch and push new changes to the repository.
    """
    inputs = {
        "branch_name": {
            "type": "string",
            "description": "the target branch that will be pushed, new or existing."
        }
    }
    output_type = "string"

    def forward(self, branch_name) -> str:
        import os
        import subprocess
        try:
            gitUsername = os.getenv("GIT_USERNAME")
            gitEmail = os.getenv("GIT_EMAIL")
            # new_branch = "add-generated-image-2"
            # Step 1: Ensure we are in a Git repository
            subprocess.run(["git", "status"], check=True)

            # Step 2: Create and switch to a new branch
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            print(f"Checked out to new branch: {branch_name}")

            # Step 3: Add the changes
            subprocess.run(["git", "add", "*"], check=True)
            print("Changes added to staging.")
            # Step 4: Add credentials
            subprocess.run(["git", "config", "--global", "user.email", gitEmail], check=True)
            print("Updated git email.")
            subprocess.run(["git", "config", "--global", "user.name", gitUsername], check=True)
            print("Updated git user name.")

            # Step 5: Commit the changes
            commit_message = "Add generated image to repository"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print("Changes committed.")

            #Step 6: Push the branch to the remote repository
            subprocess.run(["git", "push", "--set-upstream", "origin", branch_name], check=True)
            return print(f"Branch '{branch_name}' pushed to remote repository.")
        except subprocess.CalledProcessError as e:
            return print(f"An error occurred while performing Git operations: {e}")

class FindFilesTool(Tool):
    name = "find_files"
    description = "Find files with a given extension in a directory and its subdirectories"
    inputs = {"extension":{"type":"string","description":"the place from which you start your ride"}}
  
    output_type = "string"

    def forward(self, extension: str) -> str:
        """
        Recursively search for files with a given extension in a directory and its subdirectories.

        Args:
            extension: The file extension to look for (e.g., '.txt')
        """
        import os

        root_dir = "./"
        found_files = []

        # Walk through the directory tree
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(extension):
                    filepath = os.path.join(dirpath, filename)
                    absolute_path = os.path.abspath(filepath)
                    found_files.append(absolute_path)

        return found_files