
import os

def delete_subgraph_files(root_folder):
    # Iterate through all subdirectories in the root folder
    for subdir, _, files in os.walk(root_folder):

        # discussion_file = os.path.join(subdir, "CausesOfAction.subgraph")
        # if os.path.isfile(discussion_file):
        #     os.remove(discussion_file)
        #     print(f"Deleted: {discussion_file}")

        # discussion_file = os.path.join(subdir, "Ontology.subgraph")
        # if os.path.isfile(discussion_file):
        #     os.remove(discussion_file)
        #     print(f"Deleted: {discussion_file}")
                
        # discussion_file = os.path.join(subdir, "LegalPrinciples.subgraph")
        # if os.path.isfile(discussion_file):
        #     os.remove(discussion_file)
        #     print(f"Deleted: {discussion_file}")

        # discussion_file = os.path.join(subdir, "DiscussionLowerCourt.subgraph")cls
        # if os.path.isfile(discussion_file):
        #     os.remove(discussion_file)
        #     print(f"Deleted: {discussion_file}")

        # discussion_file = os.path.join(subdir, "Discussion.subgraph")
        # if os.path.isfile(discussion_file):
        #     os.remove(discussion_file)
        #     print(f"Deleted: {discussion_file}")                
            
        # discussion_file = os.path.join(subdir, "Doctrines.subgraph")
        # if os.path.isfile(discussion_file):
        #     os.remove(discussion_file)
        #     print(f"Deleted: {discussion_file}")              
        
        # Check and delete "FullScript.subgraph" if it exists
        fullscript_file = os.path.join(subdir, "LegalPrinciples.xml")
        if os.path.isfile(fullscript_file):
            os.remove(fullscript_file)
            print(f"Deleted: {fullscript_file}")

# Define the root folder
root_folder = "Output"

# Call the function to delete the files
delete_subgraph_files(root_folder)
